import pytorch_lightning as pl
import torch.utils.data
import torch
import json
import random
import math
from transformers import AutoTokenizer


class SupervisedDataModule(pl.LightningDataModule):
    def __init__(
        self,
        fname_cls: str,
        fname_not: str,
        tokenizer=AutoTokenizer.from_pretrained("distilbert-base-uncased"),
        batch_size: int = 32
    ):
        self.tokenizer = tokenizer
        self.fname_cls = fname_cls
        self.fname_not = fname_not
        self.dataset = {}
        self.batch_size = batch_size

    def load_class_dataset(self, fname, label):
        # ---- LOADING JSON
        with open(fname) as file:
            data = json.load(file)
        # ---- LABELING
        data = [(label, claims) for _, claims in data]
        # ---- TOKENIZATION
        data = [
            (
                label,
                self.tokenizer(
                    claims,
                    max_length=500,
                    truncation=True,
                )
            )
            for label, claims in data
        ]
        # ---- CREATING BATCH DICT
        data = [
            dict(
                label=label,
                tokens=encoding.input_ids,
                attention_mask=encoding.attention_mask,
            )
            for label, encoding in data
        ]
        # ---- RETURNING
        return data

    def prepare_data(self):
        data = [
            *self.load_class_dataset(self.fname_cls, torch.Tensor([1, 0])),
            *self.load_class_dataset(self.fname_not, torch.Tensor([0, 1])),
        ]
        random.shuffle(data)

        train_val_border = math.ceil(len(data) * 0.6)
        val_test_border = math.ceil(len(data) * 0.8)
        self.dataset = dict(
            train=data[:train_val_border],
            val=data[train_val_border:val_test_border],
            test=data[val_test_border:]
        )

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.dataset["train"],
            batch_size=self.batch_size,
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.dataset["val"],
            batch_size=self.batch_size,
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.dataset["test"],
            batch_size=self.batch_size,
        )
