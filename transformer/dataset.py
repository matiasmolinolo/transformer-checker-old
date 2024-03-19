from typing import List
import torch
from torch.utils.data import Dataset
import json

class DyckLanguageTokenizer:
    START_TOKEN, PAD_TOKEN, END_TOKEN = 0, 1, 2
    base_vocab = {"[start]": START_TOKEN, "[pad]": PAD_TOKEN, "[end]": END_TOKEN}

    def __init__(self, vocab: str):
        self.vocab = vocab
        self.tok_to_i = {**{tok: i + 3 for i, tok in enumerate(vocab)}, **self.base_vocab}
        self.i_to_tok = {i: tok for tok, i in self.tok_to_i.items()}

    def tokenize(self, strings: List[str], max_len = None):
        def c_to_i(c):
            if c in self.tok_to_i:
                return self.tok_to_i[c]
            raise ValueError(f"Character {c} not in vocabulary")
        
        if isinstance(strings, str):
            strings = [strings]

        if max_len is None:
            max_len = max((max(len(s) for s in strings)), 1)

        tokenized = [
            [self.START_TOKEN] + [c_to_i(c) for c in s] + [self.END_TOKEN] + [self.PAD_TOKEN] * (max_len - len(s))
            for s in strings
        ]

        return torch.tensor(tokenized)
    
    def decode(self, tokens):
        if tokens.ndim < 2:
            raise ValueError("Needs to have a batch dimension.")
        
        def i_to_c(i):
            if i < len(self.i_to_tok):
                return self.i_to_tok[i]
            raise ValueError(f"Index {i} not in vocabulary")
        
        return [
            "".join(i_to_c(i.item()) for i in seq[1:] if i != self.PAD_TOKEN and i != self.END_TOKEN)
            for seq in tokens
        ]
    
    def __repr__(self):
        return f"DyckLanguageTokenizer(vocab={self.vocab!r})"

class DyckLanguageDataset(Dataset):
    def __init__(self, file, vocab):
        self.vocab = vocab
        self.tokenizer = DyckLanguageTokenizer(vocab)
        self.data = []
        with open(file, 'r') as f:
            for line in f:
                sample = json.loads(line)
                self.data.append(sample)

        self.strings = [sample['string'] for sample in self.data]
        self.tokenized = self.tokenizer.tokenize([sample['string'] for sample in self.data])
        self.balanced = torch.tensor([sample['class'] for sample in self.data], dtype=torch.bool)

    def to(self, device):
        self.tokenized = self.tokenized.to(device)
        self.balanced = self.balanced.to(device)
        return self

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        if type(idx) == slice:
            return self.__class__(list(zip(self.strings[idx], self.balanced[idx])), self.vocab)

        return {"str": self.strings[idx], "tokens": self.tokenized[idx], "class": self.balanced[idx]}
    

    