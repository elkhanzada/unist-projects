import json
import pickle
import torch
import numpy as np

from net import Model
from util import count_parameters, reset

def main():
    reset(0)

    test_data = json.load(open('test.json', 'r'))
    embeddings = pickle.load(open('./embeddings.pkl', 'rb'))

    device = 'cuda'
    model = Model().to(device)
    model.load_state_dict(torch.load('./best.pth'))
    print('number of model param: {}'.format(count_parameters(model)))

    result = []
    for data in test_data:
        embed = []
        for t in data['sentence'].split():
            if embeddings[t] is not None:
                embed.append(embeddings[t])
        embed = np.asarray(embed)
        embed = torch.Tensor(embed).unsqueeze(0).to(device)
        pred = model(embed)
        result.append({'sentence': data['sentence'],'user_id':torch.argmax(pred).item()})

    json.dump(result, open('result.json', 'w'), indent=2)

if __name__ == '__main__':
    main()