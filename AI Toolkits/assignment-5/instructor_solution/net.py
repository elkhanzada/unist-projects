import torch.nn as nn

class Model(nn.Module):
    def __init__(self, dim_input=200, dim_output=8, dim_hidden=512, num_layers=3):
        super().__init__()
        self.dim_input = dim_input
        self.dim_output = dim_output
        self.dim_hidden = dim_hidden

        self.in_linear = nn.Linear(dim_input, dim_hidden)
        self.rnn = nn.GRU(dim_hidden, dim_hidden, num_layers=num_layers, batch_first=True)
        self.out_linear = nn.Linear(dim_hidden, dim_output)

    def forward(self, embed):
        B, T, D = embed.shape
        out = self.in_linear(embed)
        out, _ = self.rnn(out)
        out = self.out_linear(out[:, -1])

        return out
