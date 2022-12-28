import torch.nn as nn
import torch


class RNNmodel(nn.Module):
    def __init__(self, embed_dim, lstm_dim, num_layers, num_classes, max_len, word_size):
        super(RNNmodel, self).__init__()
        self.lstm_dim = lstm_dim
        self.num_classes = num_classes
        self.max_len = max_len
        self.constant_embedding = nn.Embedding(num_embeddings=word_size,
                                               embedding_dim=embed_dim
                                               )
        self.drop = nn.Dropout(0.2)
        self.lstm = nn.LSTM(input_size=embed_dim,
                            hidden_size=lstm_dim,
                            num_layers=num_layers,
                            bidirectional=True,
                            batch_first=True,
                            # dropout=0.4
                            )
        self.classifier = nn.Sequential(
            nn.BatchNorm1d(4 * lstm_dim),
            nn.Linear(
                4 * lstm_dim,
                num_classes),
        )

    def forward(self, x):
        embs = self.constant_embedding(x)
        self.lstm.flatten_parameters()
        outputs, _ = self.lstm(self.drop(embs))
        encoding = torch.cat((outputs[:, 0, :], outputs[:, -1, :]), dim=1)
        out = self.classifier(encoding)
        return out
