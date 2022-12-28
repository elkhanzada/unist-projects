import torch

def test(model, sample, device):
    model.eval()

    with torch.no_grad():
        input = sample['img'].float().to(device)
        label = sample['label'].long().to(device)

        pred = model(input)
        num_correct = torch.sum(torch.argmax(pred, dim=-1)==label)

    return num_correct.item()    


