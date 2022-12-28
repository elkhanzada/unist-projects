import torch
from torch.utils.data import Dataset
import pickle
import argparse
from dataset import TwitterData
from model import RNNmodel

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def test(model, valid_loader):
    model.eval()
    all_preds = []
    for batch_id, data in enumerate(valid_loader):
        X = data[0]
        X = X.to(device)
        pred = model(X)
        pred_ids = torch.argmax(pred.data, dim=1)
        all_preds.append(pred_ids.item())
    return all_preds


def run(filename):
    with open("idx_to_token.pkl", 'rb') as f:
        idx_to_token = pickle.load(f)
    with open("token_to_idx.pkl", 'rb') as f:
        token_to_idx = pickle.load(f)
    valid_dataset = TwitterData(filename, 50,
                                tokenizers=(idx_to_token, token_to_idx), testing=True)
    model = RNNmodel(embed_dim=50, num_layers=1, lstm_dim=256, num_classes=8,
                     max_len=50,
                     word_size=len(idx_to_token))
    model.load_state_dict(torch.load("best_model.pth"))
    valid_loader = torch.utils.data.DataLoader(valid_dataset, batch_size=1)
    model.to(device=device)
    all_preds = test(model, valid_loader)
    # print(np.sum(all_preds==valid_dataset.data_y))
    df = valid_dataset.data
    df["user_id"] = all_preds
    df.to_json("result.json", orient="records", indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitter User Classification")
    parser.add_argument("--json", default="test.json", type=str, help="json file for testing. Default: 'test.json'")
    args = parser.parse_args()
    run(args.json)
