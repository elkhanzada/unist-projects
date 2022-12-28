from test import RNNmodel, TwitterData
import pandas as pd
import torch.nn
import torchtext.vocab
import torch.nn as nn
from torch.utils.data import Dataset
import numpy as np
import matplotlib.pyplot as plt
import collections

device = 'cuda' if torch.cuda.is_available() else 'cpu'
# Params
max_len = 50
embed_dim = 50
epochs = 1000000
learning_rate = 0.0001
weight_decay = 0.0000
momentum = 0.8
batch_size = 16
clip = 0.5

# Pre-trained embedding
glove = torchtext.vocab.GloVe("twitter.27B", dim=embed_dim)

vocab_map = {
    "covid": 'coronavirus',
    'aiall': 'ai',
    'lizzo': 'singer',
    'mikmaq': 'minority',
    'randd': 'research',
    'cardis': 'cardi',
    'multiplanetary': 'planetary',
    'multiplanet': 'planet',
    'stanfords': 'stanford',
    'powerwall': 'powerhouse',
    'droneship': 'spaceport',
    'imagenet': 'dataset',
    'mikmaki': 'minority',
    'starlink': "spacex",
    'ommmmmmmmggggggggg': 'omg',
    'omgggg': 'omg',
    'wttttffff': 'wtf'
}


def train_epoch(model, train_loader, optimizer, criterion, clip):
    model.train()
    train_acc = 0
    losses = []
    for batch_id, data in enumerate(train_loader):
        optimizer.zero_grad()
        X, y = data
        X = X.to(device)
        y = y.to(device)
        pred = model(X)
        pred_ids = torch.argmax(pred.data, dim=1)
        train_acc += torch.sum(pred_ids == y) / len(pred_ids)
        loss = criterion(pred, y)
        pt = torch.exp(-loss)
        focal_loss = (0.25 * (1-pt)**2 * loss).mean()
        focal_loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()
        losses.append(focal_loss.item())
    return losses, train_acc / (batch_id + 1)


def test(model, valid_loader, criterion):
    model.eval()
    val_acc = 0
    losses = []
    for batch_id, data in enumerate(valid_loader):
        X, y = data
        X = X.to(device)
        y = y.to(device)
        pred = model(X)
        loss = criterion(pred, y)
        pred_ids = torch.argmax(pred.data, dim=1)
        val_acc += torch.sum(pred_ids == y) / len(pred_ids)
        losses.append(loss.mean().item())
    return losses, val_acc / (batch_id + 1)


def data_investigate():
    meta = pd.read_json("meta.json")
    train = pd.read_json("train.json")
    valid = pd.read_json("valid.json")
    sentences = train['sentence'].tolist()
    weird_words = []
    for token in meta['tokens'].tolist():
        value = glove[token]
        if value.max() == 0:
            weird_words.append(token)
    weird_w_counter = []
    for sent in sentences:
        for token in sent.split():
            if token in weird_words:
                weird_w_counter.append(token)
    sentences = valid['sentence'].tolist()

    for sent in sentences:
        for token in sent.split():
            if token in weird_words:
                weird_w_counter.append(token)
    counts = collections.Counter(weird_w_counter)
    print(counts)
    weird_words = set(weird_words)
    print(weird_words)
    print(len(weird_words))
    print(len(valid))
    print(len(valid[valid['user_id'] == 0]))


def train():
    criterion = torch.nn.CrossEntropyLoss(reduction='none')
    train_dataset = TwitterData("train.json", max_len, use_meta=True)
    valid_dataset = TwitterData("valid.json", max_len,
                                tokenizers=(train_dataset.idx_to_token, train_dataset.token_to_idx))
    model = RNNmodel(embed_dim=embed_dim, num_layers=1, lstm_dim=256, num_classes=train_dataset.num_classes,
                     max_len=max_len,
                     word_size=len(train_dataset.idx_to_token))
    embeds = glove.get_vecs_by_tokens(train_dataset.idx_to_token)
    print(embeds.shape)
    model.constant_embedding.weight.data.copy_(embeds)
    model.constant_embedding.weight.requires_grad = False
    model.to(device=device)
    model.load_state_dict(torch.load("best_model.pth"))
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    train_loader = torch.utils.data.DataLoader(train_dataset, shuffle=True, batch_size=batch_size)
    valid_loader = torch.utils.data.DataLoader(valid_dataset, shuffle=True, batch_size=1)
    epoch_train_losses = []
    epoch_val_losses = []
    epoch_val_accuracies = []
    early_stopping = 10
    count = 0
    best_loss = np.inf
    best_acc = -np.inf
    for epoch in range(epochs):
        train_losses, train_acc = train_epoch(model, train_loader, optimizer, criterion, clip)
        epoch_train_losses.append(np.array(train_losses).mean())
        val_losses, val_acc = test(model, valid_loader, criterion)
        epoch_val_losses.append(np.array(val_losses).mean())
        if best_acc < val_acc and best_loss > epoch_val_losses[-1]:
            best_acc = val_acc
            best_loss = epoch_val_losses[-1]
            print(f"Saving with best accuracy and loss: {best_acc}, {best_loss}")
            torch.save(model.state_dict(), "final_model.pth")
        print(f"Train acc: {train_acc}, Val acc: {val_acc}")
        print(f"Train loss: {epoch_train_losses[-1]}, Val loss: {epoch_val_losses[-1]}")
        epoch_val_accuracies.append(epoch_val_accuracies)
        if epoch > 1 and epoch_val_accuracies[-1] > epoch_val_accuracies[-2] and epoch_val_losses[-1] > \
                epoch_train_losses[-1]:
            count += 1
        else:
            count = 0
        if count == early_stopping:
            break
        if epoch % 10 == 0:
            print(f"\nBest acc: {best_acc}, Best loss: {best_loss}\n")
    plt.plot(epoch_train_losses, label="train_loss")
    plt.plot(epoch_val_losses, label="val_loss")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # data_investigate()
    train()
