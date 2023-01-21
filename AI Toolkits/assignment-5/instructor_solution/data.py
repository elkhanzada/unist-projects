from torch.utils.data import Dataset
import numpy as np

class tweetDataset(Dataset):
    def __init__(self, embeddings, tweets):
        self.embeddings = {}
        self.valid_tokens = []
        for k, v in embeddings.items():
            if v is not None:
                self.embeddings[k] = v
                self.valid_tokens.append(k)
        self.tweets = tweets
        self.num_tokens = len(self.valid_tokens)
    
    def __len__(self):
        return len(self.tweets)

    def __getitem__(self, idx):
        curr_tweet = self.tweets[idx]
        curr_uid = curr_tweet["user_id"]
        curr_sen = curr_tweet["sentence"]
        curr_emb = []
        for t in curr_sen.split():
            if t in self.valid_tokens:
                curr_emb.append(self.embeddings[t])
        curr_emb = np.asarray(curr_emb)

        sample = dict()
        sample['user_id'] = int(curr_uid)
        sample['embed'] = curr_emb

        return sample
