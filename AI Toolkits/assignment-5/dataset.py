import pickle
import collections
import pandas as pd
import torch
from torch.utils.data import Dataset
import numpy as np

class TwitterData(Dataset):
    def __init__(self, data, max_len, use_meta=True, use_freq=False, tokenizers=None, freq=1, testing=False):
        self.data = pd.read_json(data)
        self.max_len = max_len
        if not testing:
            self.num_classes = len(self.data['user_id'].unique())
        else:
            self.num_classes = 8
        if tokenizers:
            self.train = False
            self.idx_to_token, self.token_to_idx = tokenizers
        else:
            self.train = True
            self.user_vocab = get_vocab_user_based(data)
            if use_meta:
                meta = pd.read_json("meta.json")
                self.idx_to_token, self.token_to_idx = build_vocab(meta['tokens'].tolist(), freq)
            elif use_freq:
                self.idx_to_token, self.token_to_idx = build_vocab(self.data['sentence'].tolist(), freq)
        self.data_x = self.data['sentence'].tolist()
        self.testing = testing
        if not testing:
            self.data_y = np.array(self.data['user_id'].values)
        self.tokens = []

    def __len__(self):
        return len(self.data_x)

    def get_tokens(self):
        return self.tokens

    def __getitem__(self, idx):
        tokens = self.data_x[idx].split()
        if self.train:
            # rare_words = self.user_vocab[int(self.data_y[idx])]
            # tokens.append(rare_words[np.random.randint(0, len(rare_words), 1)[0]])
            if np.random.uniform(0, 1) > 0.5:
                tokens = list(filter(lambda x: np.random.uniform(0, 1) > 0.5, tokens))

        org_data = [self.token_to_idx[token] if token in self.token_to_idx else self.token_to_idx['<unk>'] for token in
                    tokens]

        self.tokens = tokens

        if len(org_data) > self.max_len:
            org_data = org_data[:self.max_len]
        else:
            for i in range(self.max_len - len(org_data)):
                org_data.append(0)
        return torch.LongTensor(org_data), int(self.data_y[idx]) if not self.testing else torch.LongTensor(org_data)






def build_vocab(texts, min_freq):
    tokens = []
    for text in texts:
        tokens.extend(text.split())
    counter = collections.Counter(tokens)
    token_freqs = sorted(counter.items(), key=lambda x: x[1],
                         reverse=True)
    idx_to_token = list(sorted(set(['<unk>'] + [
        token for token, freq in token_freqs if freq >= min_freq])))

    token_to_idx = {token: idx
                    for idx, token in enumerate(idx_to_token)}

    with open("idx_to_token.pkl", 'wb') as f:
        pickle.dump(file=f, obj=idx_to_token)
    with open("token_to_idx.pkl", 'wb') as f:
        pickle.dump(file=f, obj=token_to_idx)
    return idx_to_token, token_to_idx


def get_vocab_user_based(data):
    data = pd.read_json(data)
    user_data = [data[data['user_id'] == i]['sentence'].tolist() for i in range(8)]
    user_tokens = [[] for i in range(8)]
    for i, user in enumerate(user_data):
        for sent in user:
            user_tokens[i].extend(sent.split())
        user_tokens[i] = set(user_tokens[i])
    unique_user_tokens = []
    unique_user_tokens_dict = {}
    for i in range(len(user_tokens)):
        unique_user_tokens_dict[i] = []
        for token in user_tokens[i]:
            for j in range(len(user_tokens)):
                if i == j:
                    continue
                if token in user_tokens[j]:
                    break
            else:
                unique_user_tokens.append(token)
                unique_user_tokens_dict[i].append(token)
    return unique_user_tokens_dict