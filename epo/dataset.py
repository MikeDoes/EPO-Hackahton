import os
from typing import Iterable
from xml.etree import ElementTree as ET
from functools import lru_cache
from itertools import chain
from torch.utils.data import Dataset
import requests
import base64
import json


class WebEPODataset(Dataset):
    def __init__(
        self,
        key: str,
        secret: str,
        index: Iterable[str],  # A mapping from index to the document
    ) -> None:
        super().__init__()

        # ---- GETTING INDEX ---- #
        self.__index: list[str] = list(index)

        # ---- AUTHENTICATING API ---- #
        self.__url: str = "https://ops.epo.org"
        self.__creds: str = base64.b64encode(
            bytes(f"{key}:{secret}", "utf-8"),
        ).decode("utf-8")
        self.__auth()

    def __auth(self) -> None:
        """Renews token"""
        res = requests.post(
            f"{self.__url}/3.2/auth/accesstoken",
            "grant_type=client_credentials",
            headers={
                "Authorization": f"Basic {self.__creds}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        if not res:
            raise Exception(f"Authentication failed with {res.status_code} status code")
        self.__token = json.loads(res.content)["access_token"]

    def __get(self, path) -> requests.Response:
        get_res = lambda: requests.get(
            f"{self.__url}{path}",
            headers={
                "Authorization": f"Bearer {self.__token}",
            },
        )

        res = get_res()
        if res:
            return res
        self.__auth()
        return get_res()

    def __len__(self) -> int:
        return len(self.__index)

    @lru_cache(maxsize=1000)
    def __getitem__(self, index: int) -> str:
        res = self.__get(
            f"/rest-services/published-data/publication/epodoc/{self.__index[index]}/claims"
        )
        doc = ET.fromstring(res.content.decode("utf-8"))
        claims = doc.findall(".//{http://www.epo.org/fulltext}claim-text")
        claims = map(lambda claim: claim.text or "", claims)
        claims = "\n".join(claims)
        return claims  # TODO: Make class of the doc to be the target


class FileEPODataset(Dataset):
    def __init__(
        self,
        path: str = "./epo/data/full_text_samples",
        lang: str = "en",
    ) -> None:
        super().__init__()
        self.__filenames = [os.path.join(path, x, f"{x}.xml") for x in os.listdir(path)]
        self.__lang = lang

    def __len__(self) -> int:
        """
        Returns the size of the dataset
        """
        return len(self.__filenames)

    @lru_cache(maxsize=1000)
    def __getitem__(self, index: int) -> tuple[str, str]:
        """
        Given numeric index of the item within the dataset length
        Returns tuple of:
        - A string of newline-separated claims (filtered by language)
        - A string with the document class
        """
        doc = ET.parse(self.__filenames[index])
        claims = doc.findall(".//claim[@id]")
        claims = filter(lambda claim: f"c-{self.__lang}-" in claim.attrib["id"], claims)
        claims = map(lambda claim: claim.findall(".//claim-text"), claims)
        claims = chain(*claims)
        claims = map(lambda claim: claim.text or "", claims)
        claims = "\n".join(claims)
        return claims, ""
