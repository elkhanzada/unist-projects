import json
import pickle
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader

from net import Model
from data import tweetDataset
from trainer import train, valid
from util import reset

def main():
    reset(0)
    
    train_data = json.load(open('./train.json', 'r'))
    valid_data = json.load(open('./valid.json', 'r'))

    embeddings = pickle.load(open('./embeddings.pkl', 'rb'))

    train_dataset = tweetDataset(embeddings, train_data)
    train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    valid_dataset = tweetDataset(embeddings, valid_data)
    valid_loader = DataLoader(valid_dataset, batch_size=1, shuffle=True)

    device = 'cuda'
    model = Model().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-6)

    #############################################
    max_epoch = 10
    max_accu = -1
    for epoch in range(max_epoch):
        train_loss = 0.0
        for sample in train_loader:
            curr_loss = train(model, optimizer, sample)
            train_loss += curr_loss / len(train_loader)
        
        valid_accu = 0.0
        for sample in valid_loader:
            curr_correct = valid(model, sample)
            valid_accu += curr_correct / len(valid_dataset)

        print('[EPOCH {}] train loss: {:.03f}, valid_accu: {:.03f}'.format(epoch, train_loss, valid_accu))

        max_accu = max(max_accu, valid_accu)
        if max_accu == valid_accu:
            torch.save(model.state_dict(), './best.pth')
            print('Saving the Best model')

if __name__ == '__main__':
    main()