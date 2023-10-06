import math
import torch as t
import torch.nn as nn
t.manual_seed(0)

import matplotlib.pyplot as plt 
plt.rcParams['text.usetex'] = True

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()

N = 20

xs = t.linspace(-5, 5, 100)[:, None]
X = t.linspace(-4, 4, N)[:, None]
y = t.sin(X) + 0.5*t.randn(N, 1)

plt.scatter(x=X, y=y, label='Data', c='k')
plt.xlabel('$x$')
plt.ylabel('$y$')
#plt.plot(xs, t.sin(xs), label='"True" (noise-free) line', c='r')

input_features = 1 
hidden_features = 100
output_features = 1 

def train(p, label, alpha=1):
    net = nn.Sequential(
        nn.Linear(input_features, hidden_features),
        nn.ReLU(),
        nn.Dropout(p),
        nn.Linear(hidden_features, hidden_features),
        nn.ReLU(),
        nn.Dropout(p),
        nn.Linear(hidden_features, output_features)
    )
    opt = t.optim.Adam(net.parameters(), lr=0.03)
    net.train()

    for i in range(1000):
        i +=1
        L = ((net(X) - y)**2).mean()
        L.backward()
        opt.step()
        opt.zero_grad()

    net.eval()
    plt.plot(xs, net(xs).detach(), c='tab:orange', label=label, alpha=alpha)

train(0.0, 'No dropout', alpha=0.3)
train(0.2, 'Dropout prob=0.2', alpha=0.7)
train(0.5, 'Dropout prob=0.5')


plt.legend()
plt.savefig(args.filename, bbox_inches='tight')
