import os
from numpy import array
import torch
import torch.nn as nn
import torch.nn.functional as F
from positionClass import Position
from notation.square import BoardMove, BoardSquare
from .data import position_encode_start, position_encode_target

saved_networks_path = os.path.join(os.path.dirname(__file__), "networks")

class Start_predictor(nn.Module):
    def __init__(self):
        super(Start_predictor, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, 4, 1)
        self.conv2 = nn.Conv2d(64, 128, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 64)

    def forward(self, x) -> torch.Tensor:
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

class Target_predictor(nn.Module):
    def __init__(self):
        super(Target_predictor, self).__init__()
        self.conv1 = nn.Conv2d(13, 64, 4, 1)
        self.conv2 = nn.Conv2d(64, 128, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 64)

    def forward(self, x) -> torch.Tensor:
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

class ChessAI:
    def __init__(self, start_opn: Start_predictor, target_opn: Target_predictor, 
                       start_mid: Start_predictor, target_mid: Target_predictor, 
                       start_end: Start_predictor, target_end: Target_predictor) -> None:
        self.start_opn = start_opn
        self.target_opn = target_opn
        self.start_mid = start_mid
        self.target_mid = target_mid
        self.start_end = start_end
        self.target_end = target_end
    
    def predict(self, position: Position) -> BoardMove:
        start_prediction = torch.zeros(64)
        target_prediction = torch.zeros(64)
        if position.fullmove_number <= 15:
            start_prediction += self.start_opn(torch.tensor(array([position_encode_start(position.pos_array)]), dtype=torch.float))[0,:]
            start_id = start_prediction.argmax()
            target_prediction += self.target_opn(torch.tensor(array([position_encode_target(position.pos_array, start_id)]), dtype=torch.float))[0,:]
        if position.fullmove_number >= 15 and position.fullmove_number <= 25:
            start_prediction += self.start_mid(torch.tensor(array([position_encode_start(position.pos_array)]), dtype=torch.float))[0,:]
            start_id = start_prediction.argmax()
            target_prediction += self.target_mid(torch.tensor(array([position_encode_target(position.pos_array, start_id)]), dtype=torch.float))[0,:]
        if position.fullmove_number >= 25:
            start_prediction += self.start_end(torch.tensor(array([position_encode_start(position.pos_array)]), dtype=torch.float))[0,:]
            start_id = start_prediction.argmax()
            target_prediction += self.target_end(torch.tensor(array([position_encode_target(position.pos_array, start_id)]), dtype=torch.float))[0,:]
        target_id = int(target_prediction.argmax())
        return BoardMove(BoardSquare(start_id%8, start_id//8), BoardSquare(target_id%8, target_id//8))


def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            if args.dry_run:
                break

def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

def load_start_predictor(filename: str) -> Start_predictor:
    model = Start_predictor()
    model.load_state_dict(torch.load(os.path.join(saved_networks_path, filename), weights_only=True))
    model.eval()
    return model

def load_target_predictor(filename: str) -> Target_predictor:
    model = Target_predictor()
    model.load_state_dict(torch.load(os.path.join(saved_networks_path, filename), weights_only=True))
    model.eval()
    return model

def load_chessAI(start_opn_file: str, target_opn_file: str, 
                 start_mid_file: str, target_mid_file: str, 
                 start_end_file: str, target_end_file: str) -> ChessAI:
    start_opn = load_start_predictor(start_opn_file)
    target_opn = load_target_predictor(target_opn_file)
    start_mid = load_start_predictor(start_mid_file)
    target_mid = load_target_predictor(target_mid_file)
    start_end = load_start_predictor(start_end_file)
    target_end = load_target_predictor(target_end_file)
    return ChessAI(start_opn, target_opn, start_mid, target_mid, start_end, target_end)