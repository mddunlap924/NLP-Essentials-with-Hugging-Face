import numpy as np
from typing import Type, TypeVar, List, Dict, Union
from datasets import Dataset
import unicodedata
from unidecode import unidecode
import codecs
import re
from omegaconf.dictconfig import DictConfig
from itertools import chain
import string
import itertools
import torch
from sklearn.preprocessing import (LabelEncoder,
                                   OneHotEncoder)
from dataclasses import dataclass


T = TypeVar('T')


def view_tokens(tok: Type[T], input_ids: list) -> None:
    """Decode and Print input_ids tokens for viewing

    Args:
        tok (Type[T]): Tokenizer
        input_ids (list): List of input_id tokens
    """
    print(f'input_ids:\n{input_ids}\n\n')
    print(f'tokenizer.convert_ids_to_tokens(input_ids):\n'
          f'{tok.convert_ids_to_tokens(input_ids)}\n\n')

    print(f'tokenizer.decode(input_ids):\n'
          f'{tok.decode(input_ids)}\n')
    return


def left_or_right(example: Type[T],
                  tokenizer: Type[T],
                  cfg: dataclass) -> Dataset:
    # Tokenize
    tokenizer.truncation_side = cfg.truncation_side
    if cfg.max_length is None:
        tk = tokenizer(text=example['text'],
                       truncation=cfg.truncation,
                       padding=cfg.padding,
                       return_length=cfg.return_length)
    else:
        tk = tokenizer(text=example['text'],
                       truncation=cfg.truncation,
                       padding=cfg.padding,
                       max_length=cfg.max_length,
                       return_length=cfg.return_length)
    return {**tk}


class CustomTokenizer:
    def __init__(self, cfg: dataclass, tokenizer: Type[T]):
        self.cfg = cfg
        self.tokenizer = tokenizer

    def left_or_right(self,
                      example: Type[T]) -> Dataset:

        # Tokenize
        self.tokenizer.truncation_side = self.cfg.truncation_side
        if self.cfg.max_length is None:
            tk = self.tokenizer(text=example['text'],
                                truncation=self.cfg.truncation,
                                padding=self.cfg.padding,
                                return_length=self.cfg.return_length)
        else:
            tk = self.tokenizer(text=example['text'],
                                truncation=self.cfg.truncation,
                                padding=self.cfg.padding,
                                max_length=self.cfg.max_length,
                                return_length=self.cfg.return_length)
        return {**tk}
