import glob
import os.path

import pandas as pd


def load_uwb_data(base_path, data_type):
    files = []

    for room in ['f8', 'f10']:
        path = os.path.join(base_path, room, data_type, '*.csv')
        found = glob.glob(path)
        files.append(found)

    if not files:
        raise IOError(f"No csv files found in provided resource directory (base_path: {base_path}, data_type: {data_type})")

    csvs = []
    for file in files:
        csv = pd.read_csv(file, header=None)
        csvs.append(csv)

    concated_csvs = pd.concat(csvs, ignore_index=True)

    measurements = concated_csvs.iloc[:, 0:2].values
    real_data = concated_csvs.iloc[:, 2:4].values

    return measurements, real_data