import argparse
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from chessAI import Start_predictor, Target_predictor, train, test, load_predictor
from chessAI.data import Games
from time import perf_counter

parser = argparse.ArgumentParser(description='Chess-predictor')
parser.add_argument('--batch-size', type=int, default=100, metavar='N',
                    help='input batch size for training (default: 64)')
parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                    help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=6, metavar='N',
                    help='number of epochs to train (default: 14)')
parser.add_argument('--lr', type=float, default=1.0, metavar='LR',
                    help='learning rate (default: 1.0)')
parser.add_argument('--gamma', type=float, default=1, metavar='M',
                    help='Learning rate step gamma (default: 0.7)')
parser.add_argument('--no-accel', action='store_true',
                    help='disables accelerator')
parser.add_argument('--dry-run', action='store_true', default=False, 
                    help='quickly check a single pass')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
parser.add_argument('--save-model', action='store_true', default=True,
                    help='For Saving the current Model')
args = parser.parse_args()

use_accel = not args.no_accel and torch.accelerator.is_available()

torch.manual_seed(args.seed)

if use_accel:
    device = torch.accelerator.current_accelerator()
else:
    device = torch.device("cpu")

train_kwargs = {'batch_size': args.batch_size}
test_kwargs = {'batch_size': args.test_batch_size}
if use_accel:
    accel_kwargs = {'num_workers': 4,
                    'persistent_workers': True,
                    'pin_memory': True,
                    'shuffle': True}
    train_kwargs.update(accel_kwargs)
    test_kwargs.update(accel_kwargs)

isstart = True
t1 = perf_counter()
dataset1 = Games("data10.txt", 0, 300_000, False, isstart=isstart)
t2 = perf_counter()
print(t2-t1)
dataset2 = Games("data10.txt", 300_000, 300_000 + 10_000, False, isstart=isstart)
#dataset1 = Games("data.txt", 0, 200, False, isstart)
#dataset2 = Games("data.txt", 200, 210, False, isstart)

train_loader = torch.utils.data.DataLoader(dataset1,**train_kwargs)
test_loader = torch.utils.data.DataLoader(dataset2, **test_kwargs)


model = Start_predictor().to(device)
#model = Target_predictor().to(device)
optimizer = optim.Adadelta(model.parameters(), lr=args.lr)

scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)
for epoch in range(1, args.epochs + 1):
    train(args, model, device, train_loader, optimizer, epoch)
    test(model, device, test_loader)
    scheduler.step()

if args.save_model:
    torch.save(model.state_dict(), "chessAI/networks/start1.pt")