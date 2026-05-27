import torch
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler

from util.AdjustUWBDataNet import train_model
from util.data_loader import load_uwb_data
from util.parser import parse_args, show_args

if __name__ == "__main__":
    args = parse_args()
    print("Uruchomiono uczenie z parametrami")
    show_args(args)
    print()

    # load data
    print("Ładuje dane")
    print()
    measurements_train_raw, real_train_raw = load_uwb_data(base_path=args.source, data_type='stat')
    measurements_test_raw, real_test_raw = load_uwb_data(base_path=args.source, data_type='dyn')
    print("Dane załadowano:")
    print(f"Pomiarow treningowych statycznych: {measurements_train_raw.size}")
    print(f"Pomiarow testowych dynamicznych: {measurements_test_raw.size}")
    print(f"Rzeczywistych treningowych wartosci statycznych: {real_train_raw.size}")
    print(f"Rzeczywistych testowych wartosci dynamicznych: {real_test_raw.size}")
    print()

    print("Zaczynam normalizacje danych")
    if args.scaler == 'minmax':
        scaler_measurements, scaler_real = MinMaxScaler(), MinMaxScaler()
    elif args.scaler == 'maxabs':
        scaler_measurements, scaler_real = MaxAbsScaler(), MaxAbsScaler()
    else:
        scaler_measurements, scaler_real = StandardScaler(), StandardScaler()
    print("Zakonczylem normalizacje danych")
    print()

    measurements_train = torch.tensor(scaler_measurements.fit_transform(measurements_train_raw), dtype=torch.float)
    real_train = torch.tensor(scaler_real.fit_transform(real_train_raw), dtype=torch.float)
    measurements_test = torch.tensor(scaler_measurements.fit_transform(measurements_test_raw), dtype=torch.float)
    real_test = torch.tensor(scaler_real.fit_transform(real_test_raw), dtype=torch.float)

    # TODO: finish data collection and results viewing, add descriptions to program to show what it is doing when console freezes
    print("Rozpoczynam wykonywanie wlasciwego programu:")
    for i in range(args.runs):
        print(f"Niezalezne podejscie nr {i+1}")

        model, h_train, h_test = train_model(args, measurements_train, real_train, measurements_test, real_test)
    print()

    print("Zakonczylem dzialanie programu")
    print(model, h_train, h_test)

