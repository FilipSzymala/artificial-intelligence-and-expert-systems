import torch
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler

from util.AdjustUWBDataNet import train_model
from util.data_loader import load_uwb_data
from util.parser import parse_args, show_args

if __name__ == "__main__":
    args = parse_args()

    # load data
    measurements_train_raw, real_train_raw = load_uwb_data(base_path=args.source, data_type='stat')
    measurements_test_raw, real_test_raw = load_uwb_data(base_path=args.source, data_type='dyn')

    if args.scaler == 'minmax':
        scaler_measurements, scaler_real = MinMaxScaler(), MinMaxScaler()
    elif args.scaler == 'maxabs':
        scaler_measurements, scaler_real = MaxAbsScaler(), MaxAbsScaler()
    else:
        scaler_measurements, scaler_real = StandardScaler(), StandardScaler()

    measurements_train = torch.tensor(scaler_measurements.fit_transform(measurements_train_raw), dtype=torch.float)
    real_train = torch.tensor(scaler_real.fit_transform(real_test_raw), dtype=torch.float)
    measurements_test = torch.tensor(scaler_measurements.fit_transform(measurements_train_raw), dtype=torch.float)
    real_test = torch.tensor(scaler_real.fit_transform(real_test_raw), dtype=torch.float)

    # TODO: finish data collection and results viewing, add descriptions to program to show what it is doing when console freezes
    # for i in range(args.runs):
    #     model = train_model(args, measurements_train, real_train, measurements_test, real_test)
    #

