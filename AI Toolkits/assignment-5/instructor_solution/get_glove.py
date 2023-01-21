import json
import numpy as np
import pickle

meta = json.load(open('meta.json', 'r'))

tokens = meta['tokens']
embeddings = {t:None for t in tokens}
cnt = 0 
with open('glove.twitter.27B.200d.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line: break
        if line.split()[0] in tokens:
            embeddings[line.split()[0]] = np.asarray([float(t) for t in line.split()[1:]])
        cnt += 1
        if cnt % 100000 == 0:
            print(cnt)

pickle.dump(embeddings, open('embeddings.pkl', 'wb'))
