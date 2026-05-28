import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from util.data_loader import load_uwb_data

# ==========================================
# CONFIG
# ==========================================
BEST_MODELS = {
    'ReLU': {'mse': './out/relu_var1_mse.csv', 'out': './out/relu_var1_output.csv', 'color': 'green'},
    'Tanh': {'mse': './out/tanh_var5_mse.csv', 'out': './out/tanh_var5_output.csv', 'color': 'orange'},
    'Logistic': {'mse': './out/logistic_var5_mse.csv', 'out': './out/logistic_var5_output.csv', 'color': 'blue'}
}

ABSOLUTE_BEST_NAME = 'ReLU'

SCALER_TYPE = 'minmax'
DATA_SOURCE_PATH = '../resource/dane'

DPI_CONFIG=300

# ==========================================

print("Ładowanie i przygotowanie danych referencyjnych...")
_, real_train_raw = load_uwb_data(base_path=DATA_SOURCE_PATH, data_type='stat')
measurements_test_raw, real_test_raw = load_uwb_data(base_path=DATA_SOURCE_PATH, data_type='dyn')

if SCALER_TYPE == 'minmax':
    scaler_real = MinMaxScaler()
elif SCALER_TYPE == 'maxabs':
    scaler_real = MaxAbsScaler()
else:
    scaler_real = StandardScaler()

scaler_real.fit(real_train_raw)

scaled_measured_test = scaler_real.transform(measurements_test_raw)
scaled_real_test = scaler_real.transform(real_test_raw)
baseline_mse = np.mean((scaled_measured_test - scaled_real_test) ** 2)


def calculate_euclidean_error(pred_points, real_points):
    return np.sqrt(np.sum((pred_points - real_points) ** 2, axis=1))


baseline_errors = calculate_euclidean_error(np.array(measurements_test_raw), np.array(real_test_raw))

plt.rcParams.update({'font.size': 11})

# --- OBLICZANIE WSPÓLNEJ SKALI Y (LOGARYTMICZNEJ) DLA WYKRESU 1 I 2 ---
all_mse_values = []
for paths in BEST_MODELS.values():
    df_mse = pd.read_csv(paths['mse'], header=None, names=['train_mse', 'test_mse'])
    all_mse_values.extend(df_mse['train_mse'][1:].tolist())
    all_mse_values.extend(df_mse['test_mse'][1:].tolist())

y_axis_min = min(all_mse_values) * 0.7
y_axis_max = max(max(all_mse_values), baseline_mse) * 1.5

def setup_log_axis(ax):
    ax.set_yscale('log')
    ax.set_ylim(y_axis_min, y_axis_max)
    ax.grid(True, which="major", linestyle='-', linewidth=0.8, color='gray', alpha=0.5)
    ax.grid(True, which="minor", linestyle='--', linewidth=0.5, color='gray', alpha=0.3)

    # Wymuszenie wyświetlania wartości liczbowych na gęstszej podziałce (minor ticks)
    # Formater zamienia brzydkie notacje naukowe na czytelne ułamki, np. 0.005
    formatter = FuncFormatter(lambda y, _: '{:g}'.format(y))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)
    # ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10))


# =====================================================================
# WYKRES 1: MSE (train batch)
# =====================================================================
print("Generowanie Wykresu 1 (MSE Treningowe)...")
fig, ax = plt.subplots(figsize=(8, 6))

for name, paths in BEST_MODELS.items():
    df_mse = pd.read_csv(paths['mse'], header=None, names=['train_mse', 'test_mse'])
    ax.plot(df_mse['train_mse'], label=name, color=paths['color'], linewidth=2)

ax.set_title('MSE - zbiór treningowy (dane statyczne)')
ax.set_xlabel('Epoka')
ax.set_ylabel('Błąd średniokwadratowy (MSE)')
setup_log_axis(ax)
ax.legend()

plt.tight_layout()
plt.savefig('./out/wykres_1_mse_train.png', dpi=DPI_CONFIG)
plt.close()

# =====================================================================
# WYKRES 2: MSE (test batch)
# =====================================================================
print("Generowanie Wykresu 2 (MSE Testowe)...")
fig, ax = plt.subplots(figsize=(8, 6))

for name, paths in BEST_MODELS.items():
    df_mse = pd.read_csv(paths['mse'], header=None, names=['train_mse', 'test_mse'])
    ax.plot(df_mse['test_mse'], label=name, color=paths['color'], linewidth=2)

ax.axhline(y=baseline_mse, color='red', linestyle='--', linewidth=2, label='MSE surowych pomiarów UWB')

ax.set_title('MSE - zbiór testowy (dane dynamiczne)')
ax.set_xlabel('Epoka')
ax.set_ylabel('Błąd średniokwadratowy MSE')
setup_log_axis(ax)
ax.legend()

plt.tight_layout()
plt.savefig('./out/wykres_2_mse_test.png', dpi=DPI_CONFIG)
plt.close()

# =====================================================================
# WYKRES 3: Dystrybuanta (CDF) Błędów Fizycznych
# =====================================================================
print("Generowanie Wykresu 3 (Dystrybuanta)...")
plt.figure(figsize=(8, 6))

sorted_base_err = np.sort(baseline_errors)
p_base = np.arange(1, len(sorted_base_err) + 1) / len(sorted_base_err)
plt.plot(sorted_base_err, p_base, color='black', linestyle='--', linewidth=2, label='Surowe pomiary UWB')

for name, paths in BEST_MODELS.items():
    df_out = pd.read_csv(paths['out'], header=None)
    model_errors = calculate_euclidean_error(df_out.values, np.array(real_test_raw))
    sorted_err = np.sort(model_errors)
    p = np.arange(1, len(sorted_err) + 1) / len(sorted_err)
    plt.plot(sorted_err, p, label=name, color=paths['color'], linewidth=2)

plt.title('Dystrybuanty błędów pozycjonowania')
plt.xlabel('Błąd bezwzględny odległości [mm]')
plt.ylabel('Prawdopodobieństwo (Dystrybuanta)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, np.percentile(baseline_errors, 80))
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('./out/wykres_3_cdf.png', dpi=DPI_CONFIG)
plt.close()

# =====================================================================
# WYKRES 4: Mapa Rzeczywista - Wykres punktowy (Zwycięzca)
# =====================================================================
print(f"Generowanie Wykresu 4 (Scatter) dla absolutnego zwycięzcy: {ABSOLUTE_BEST_NAME}...")
plt.figure(figsize=(8, 8))

df_best_out = pd.read_csv(BEST_MODELS[ABSOLUTE_BEST_NAME]['out'], header=None)
real_x, real_y = np.array(real_test_raw)[:, 0], np.array(real_test_raw)[:, 1]
raw_x, raw_y = np.array(measurements_test_raw)[:, 0], np.array(measurements_test_raw)[:, 1]
corr_x, corr_y = df_best_out.values[:, 0], df_best_out.values[:, 1]

plt.scatter(raw_x, raw_y, color='lightgray', s=3, alpha=0.8, zorder=1, label='Zmierzone UWB dynamiczne')
plt.scatter(corr_x, corr_y, color='red', s=3, alpha=0.9, zorder=2,
            label=f'Skorygowane pomiary ({ABSOLUTE_BEST_NAME})')
plt.scatter(real_x, real_y, color='black', s=3, alpha=1.0, zorder=3, label='Wartości rzeczywiste')

plt.title(f'Skorygowane wyniki UWB wraz z surowymi pomiarami dynamicznymi\n({ABSOLUTE_BEST_NAME})')
plt.xlabel('Współrzędna X [mm]')
plt.ylabel('Współrzędna Y [mm]')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='best')
plt.axis('equal')

plt.tight_layout()
plt.savefig('./out/wykres_4_scatter.png', dpi=DPI_CONFIG)
plt.close()

print("✅ ZAKOŃCZONO! 4 osobne wykresy (PNG) czekają w folderze 'out'.")