import torch.nn as nn
import torch

def train(model, optimizer, sample, device='cuda'):
    model.train()

    criteria = nn.CrossEntropyLoss()

    pred = model(sample['embed'].float().to(device))
    gt = sample['user_id'].long().to(device)

    loss = criteria(pred, gt)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()

def valid(model, sample, device='cuda'):
    model.eval()

    pred = model(sample['embed'].float().to(device))
    gt = sample['user_id'].long().to(device)

    pred_id = torch.argmax(pred)

    return pred_id.item() == gt.item()
