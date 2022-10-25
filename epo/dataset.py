import os
import sys
from xml.etree import ElementTree as ET
from functools import lru_cache
from itertools import chain

from torch.utils.data import Dataset


class EPODataset(Dataset):
    def __init__(
        self,
        path: str = "./epo/data/full_text_samples",
        lang: str = "en",
    ) -> None:
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


print(EPODataset()[0])
