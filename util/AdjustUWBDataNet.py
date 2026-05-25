import torch
from torch import nn
from torch import optim
from torch.utils.data import TensorDataset, DataLoader


class AdjustUWBDataNet(nn.Module):
    def __init__(self, hidden_neurons, activation_name):
        super().__init__()

        activations = {
            'relu': nn.ReLU(),
            'tanh': nn.Tanh(),
            'logistic': nn.Sigmoid()
        }

        self.layers = nn.Sequential(
            nn.Linear(2, hidden_neurons),
            activations[activation_name],
            nn.Linear(hidden_neurons, 2)
        )

    def forward(self, x):
        return self.layers(x)

def train_model(args, train_data, train_correct_data, test_data, test_correct_data):
    model = AdjustUWBDataNet(args.neurons, args.activation)

    if args.optimizer == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=args.learning_rate, betas=(args.beta1, args.beta2))
    else:
        optimizer = optim.SGD(model.parameters(), lr=args.learning_rate, momentum=args.beta1)

    criterion = nn.MSELoss()

    history_train = []
    history_test = []

    datatest = TensorDataset(train_data, train_correct_data)

    train_loader = DataLoader(datatest, batch_size=args.batch_size, shuffle=True)

    for epoch in range(args.epochs):
        model.train()
        epoch_loss = 0.0

        for batch_data, batch_correct_data in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_data)
            loss = criterion(predictions, batch_correct_data)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * batch_data.size(0)

        avg_train_loss = epoch_loss / len(train_loader.dataset)

        model.eval()
        with torch.no_grad():
            predictions_test = model(test_data)
            loss_test = criterion(predictions_test, test_correct_data)


        history_train.append(avg_train_loss)
        history_test.append(loss_test.item())
        
    return model, history_train, history_test