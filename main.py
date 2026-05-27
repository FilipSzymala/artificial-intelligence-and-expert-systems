import pandas as pd
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
    print(f"Pomiarow treningowych statycznych: {len(measurements_train_raw)}")
    print(f"Pomiarow testowych dynamicznych: {len(measurements_test_raw)}")
    print(f"Rzeczywistych treningowych wartosci statycznych: {len(real_train_raw)}")
    print(f"Rzeczywistych testowych wartosci dynamicznych: {len(real_test_raw)}")
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
    measurements_test = torch.tensor(scaler_measurements.transform(measurements_test_raw), dtype=torch.float)
    real_test = torch.tensor(scaler_real.transform(real_test_raw), dtype=torch.float)

    print("Rozpoczynam uczenie sieci:")
    best_mse = float("inf")
    best_model = None
    best_mse_history = []
    best_model_output =  []
    for i in range(args.runs):
        print(f"Niezalezne podejscie nr {i+1}")

        model, h_train, h_test, predictions_test = train_model(args, measurements_train, real_train, measurements_test, real_test)
        if h_test[-1] < best_mse:
            best_mse = h_test[-1]
            best_model = model
            best_mse_history = list(zip(h_train, h_test))
            best_model_output = scaler_real.inverse_transform(predictions_test)
    print()
    print("Zakonczylem uczenie sieci oraz wyloniłem najlepsza z nich")

    print(f"Najlepszy model to {best_model} i osiagnal on następujący blad sredniokwadratowy: {best_mse}")
    print()
    print("Zapisuje historie uczenia oraz historię testu dla najlepszego modelu")
    pd.DataFrame(best_mse_history).to_csv("./out/best_mse.csv", index=False, header=False)
    print("Zakończnono powodzeniem")
    print("Zapisuję wyniki otrzymane ")
    pd.DataFrame(best_model_output).to_csv("./out/best_output.csv", index=False, header=False)
    print("Zakończnono powodzeniem")
