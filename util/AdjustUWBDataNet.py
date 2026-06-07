import copy
import torch
from torch import nn
from torch import optim
from torch.utils.data import TensorDataset, DataLoader

class AdjustUWBDataNet(nn.Module):
    def __init__(self, hidden_neurons, activation_name, drop_out_rate, init_mode='default'):
        super().__init__()

        activations = {
            'relu': nn.ReLU(),
            'tanh': nn.Tanh(),
            'logistic': nn.Sigmoid()
        }

        self.layers = nn.Sequential(
            nn.Linear(2, hidden_neurons),
            activations[activation_name],
            nn.Dropout(p=drop_out_rate),
            nn.Linear(hidden_neurons, 2)
        )

        self.init_mode = init_mode
        if self.init_mode != 'default':
            self.layers.apply(self.init_weights)


    def init_weights(self, module):
        if isinstance(module, nn.Linear):
            if self.init_mode == 'xavier':
                nn.init.xavier_uniform_(module.weight)
            elif self.init_mode == 'kaiming':
                nn.init.kaiming_uniform_(module.weight, nonlinearity='relu')
            elif self.init_mode == 'uniform':
                nn.init.uniform_(module.weight, -0.1, 0.1)

    def forward(self, x):
        return self.layers(x)

def train_model(args, train_data, train_correct_data, test_data, test_correct_data):
    model = AdjustUWBDataNet(args.neurons, args.activation, args.drop_out_rate, args.init_weights)

    if args.optimizer == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=args.learning_rate, betas=(args.beta1, args.beta2))
    else:
        optimizer = optim.SGD(model.parameters(), lr=args.learning_rate, momentum=args.beta1)

    criterion = nn.MSELoss()

    history_train = []
    history_test = []

    datatest = TensorDataset(train_data, train_correct_data)
    train_loader = DataLoader(datatest, batch_size=args.batch_size, shuffle=True)

    # early stopping mechanism
    patience = args.patience
    is_early_stop = patience > 0
    best_loss = float('inf')
    epochs_no_improve = 0
    best_model_weights = None
    early_stop_triggered = False
    early_stop_epoch = None

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
            current_test_loss = loss_test.item()

        history_train.append(avg_train_loss)
        history_test.append(loss_test.item())

        if is_early_stop:
            if current_test_loss < best_loss:
                best_loss = current_test_loss
                epochs_no_improve = 0
                best_model_weights = copy.deepcopy(model.state_dict())
            else:
                epochs_no_improve += 1
                if epochs_no_improve >= patience:
                    early_stop_triggered = True
                    early_stop_epoch = epoch + 1
                    break

    if is_early_stop and best_model_weights is not None:
        model.load_state_dict(best_model_weights)

    model.eval()
    with torch.no_grad():
        final_predictions = model(test_data)

        final_loss = criterion(final_predictions, test_correct_data).item()

    return model, history_train, history_test, final_loss, final_predictions.numpy(), early_stop_triggered, early_stop_epoch
