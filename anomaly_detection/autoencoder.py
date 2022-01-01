import sys
import pandas as pd
import numpy as np
import pickle

import torch
from torch import nn
from torch import optim
from torch.utils.data import TensorDataset, DataLoader
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from tokens import NLPVectorizor

class AEWrapper(nn.Module):
    def __init__(self, batch_size, seq_len, vocab_size, model_size=None, model_depth=None):
        super(AEWrapper, self).__init__()
        #self.input_size = input_size

        self.batch_size = batch_size
        self.seq_len = seq_len
        self.vocab_size = vocab_size

        self.model_size = model_size
        self.model_depth = model_depth

        self.activation = nn.ReLU()
        self.sigmoid    = nn.Sigmoid()
        self.layers = nn.ModuleDict({
            'embedding': nn.Embedding(self.vocab_size, 300),
            'encode_1': nn.LSTM(300, 128, dropout=0, bias=False, batch_first=True),
            'encode_2': nn.LSTM(128, 64, dropout=0, bias=False, batch_first=True),
            'decode_1': nn.LSTM(64, 64, dropout=0, bias=False,batch_first=True),
            'decode_2': nn.LSTM(64, 128, dropout=0, bias=False, batch_first=True),
            'linear': nn.Linear(128, 300, bias=False)
        })

    def forward(self, input, input_len):
        input_emb  = self.layers['embedding'](input)

        x, (_, _) = self.layers['encode_1'](input_emb)
        x         = self.activation(x)

        _, (x, _) = self.layers['encode_2'](x)
        x         = self.activation(x)

        x         = x.repeat(1, seq_len, 1)

        x, (_, _) = self.layers['decode_1'](x)
        x         = self.activation(x)

        x, (_, _) = self.layers['decode_2'](x)
        x         = self.activation(x)

        x         = self.layers['linear'](x)
        x         = self.sigmoid(x)

        return input_emb, x

def trainModel(model, x_train, num_epochs=3, batch_size=1, print_n_batches=100):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.02)

    train_loader = DataLoader(x_train, batch_size=batch_size)
    for epoch in range(num_epochs):

        running_loss = 0.0
        for i, (input, input_len) in enumerate(train_loader, 0):
            # Forward + backward
            optimizer.zero_grad()
            input_emb, output = model(input, input_len)

            # Unpack and backprop
            loss = criterion(input_emb, output)
            loss.backward()
            optimizer.step()

            # Print statistics
            running_loss += loss.item() * 1000
            if i % print_n_batches == (print_n_batches - 1):    # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / print_n_batches))
                running_loss = 0.0

    return model

def detectAnomalies(model, x_test, threshold):
    criterion = nn.MSELoss()

    train_loader = DataLoader(x_test, batch_size=batch_size)

    with torch.no_grad():

        inputs = []
        losses = []
        for i, (input, input_len) in enumerate(train_loader, 0):
            input_emb, output = model(input, input_len)
            loss = criterion(input_emb, output)

            inputs.append(input)
            losses.append(loss.item())

        return inputs, losses

if __name__ == '__main__':
    '''
    messages = [
        'apples are super good and tasty',
        'bananas are also very delicious',
        'peaches taste like heaven',
        "oranges can't be beat",
        'apricots are the best thing and super awesome',
    ]
    '''

    # Hyperparameters
    batch_size = 1
    seq_len = 70

    # Load data
    #data_df = pd.read_csv('parsed_emails.csv', sep='|')
    #messages = list(data_df['body'])[:1000]
    data_df = pd.read_csv('trumptweets.csv')
    messages = data_df['content'][:1000]

    # Vectorize
    nlp_vectorizor = NLPVectorizor(max_sentence_size=seq_len)
    nlp_vectorizor.fit(messages)
    x_train = nlp_vectorizor.transform(messages)
    #pickle.dump(x_train, open('x_train.pkl', 'wb'))

    # Train model
    print(len(nlp_vectorizor.nlp.vocab))
    lstm_ae = AEWrapper(batch_size, seq_len, len(nlp_vectorizor.nlp.vocab))
    lstm_ae = trainModel(lstm_ae, x_train)

    messages = []
    messages.append("make america great again")

    x_test = nlp_vectorizor.transform(messages)

    inputs, losses = detectAnomalies(lstm_ae, x_test, 10)
    messages_losses = zip(messages, losses)
    messages_losses = sorted(messages_losses, key=lambda ml: ml[1])
    print(messages_losses[:10])
