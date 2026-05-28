#
# Generowanie wykresów do sprawozdania z zadania 2 (UWB)
# ======================================================
# Dla KAŻDEJ funkcji aktywacji (relu, tanh, logistic) generujemy zestaw 4 wykresów.
# Wszystkie warianty dla danej funkcji znajdują się na jednym wykresie liniowym,
# każdy oznaczony innym kolorem. Wykres 4 (punktowy) rysowany jest tylko dla
# najlepszego wariantu z danej grupy.

import glob
import os
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler
from util.data_loader import load_uwb_data

# ==============================================================================
# KONFIGURACJA
# ==============================================================================

DATA_SOURCE_PATH = '../resource/dane'

# MUST BE SAME AS IN main.py
SCALER_TYPE = 'minmax'

OUT_DIR   = '../out'
PLOTS_DIR = '../out/plots'

# Przyjazne nazwy wariantów do legendy na wykresach
VARIANT_NAMES = {
    1: 'W1: Baza (16n, bez dropoutu)',
    2: 'W2: Szersza (32n, mały batch)',
    3: 'W3: Potężna (64n, wolny skok)',
    4: 'W4: Szybki skok (16n, duży LR)',
    5: 'W5: Złoty Środek (32n, precyzja)'
}

# Paleta kolorów dla wariantów
VARIANT_COLORS = [
    '#27ae60', # Zielony
    '#e74c3c', # Czerwony
    '#2980b9', # Niebieski
    '#8e44ad', # Fioletowy
    '#f39c12', # Pomarańczowy
    '#16a085', # Morski
    '#2c3e50', # Granatowy
    '#d35400'  # Ceglasty
]

MSE_YMAX = None
MSE_LOG_SCALE = True
CDF_PERCENTILE_ZOOM = 85

FIG_SIZE_MSE     = (8, 5)
FIG_SIZE_CDF     = (9, 5)
FIG_SIZE_SCATTER = (8, 8)
SAVE_DPI = 300

# ==============================================================================
# FUNKCJE POMOCNICZE
# ==============================================================================

def make_scalers(scaler_type):
    mapping = {
        'minmax':   (MinMaxScaler,   MinMaxScaler),
        'maxabs':   (MaxAbsScaler,   MaxAbsScaler),
        'standard': (StandardScaler, StandardScaler),
    }
    A, B = mapping[scaler_type]
    return A(), B()

def euclidean_error(a, b):
    return np.sqrt(np.sum((a - b) ** 2, axis=1))

def setup_mse_axis(ax, y_min, y_max, log_scale):
    if log_scale:
        ax.set_yscale('log')
        fmt = mticker.FuncFormatter(lambda y, _: f'{y:g}')
        ax.yaxis.set_major_formatter(fmt)
        ax.yaxis.set_minor_formatter(fmt)
        ax.yaxis.set_minor_locator(
            mticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10)
        )
        ax.grid(True, which='major', linestyle='-',  linewidth=0.8, color='gray', alpha=0.4)
        ax.grid(True, which='minor', linestyle='--', linewidth=0.4, color='gray', alpha=0.25)
    else:
        ax.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.4)
    ax.set_ylim(y_min, y_max)

def scan_variants(out_dir):
    # Groups available variants by activation func
    activations = ['relu', 'tanh', 'logistic']
    grouped_variants = {act: [] for act in activations}

    for act in activations:
        pattern = os.path.join(out_dir, f'{act}_var*_mse.csv')
        for mse_path in sorted(glob.glob(pattern)):
            out_path = mse_path.replace('_mse.csv', '_output.csv')
            if not os.path.exists(out_path):
                print(f"Brak {os.path.basename(out_path)} — pominięto.")
                continue

            match = re.search(r'_var(\d+)_mse\.csv$', mse_path)
            var_num = int(match.group(1)) if match else 0

            label_name = VARIANT_NAMES.get(var_num, f'Wariant {var_num}')

            grouped_variants[act].append({
                'activation': act,
                'variant':    var_num,
                'label':      label_name,
                'mse_path':   mse_path,
                'out_path':   out_path,
            })

    return {k: v for k, v in grouped_variants.items() if len(v) > 0}

def plot_activation_group(activation_name, variants_list, measurements_test, real_test,
                          baseline_mse, baseline_errors, mse_y_min, mse_y_max, cdf_xlim, plots_dir):
    prefix = os.path.join(plots_dir, f"{activation_name}")
    act_title = activation_name.capitalize()

    for v in variants_list:
        v['df_mse'] = pd.read_csv(v['mse_path'], header=None, names=['train', 'test'])
        v['preds'] = pd.read_csv(v['out_path'], header=None).values
        v['errors'] = euclidean_error(v['preds'], real_test)
        v['median_err'] = float(np.median(v['errors']))
        v['min_mse'] = float(v['df_mse']['test'].min())

    variants_list.sort(key=lambda x: x['variant'])

    best_variant = min(variants_list, key=lambda x: x['median_err'])

    # ------------------------------------------------------------------
    # Wykres 1: MSE — zbiór uczący
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=FIG_SIZE_MSE)
    for i, v in enumerate(variants_list):
        color = VARIANT_COLORS[i % len(VARIANT_COLORS)]
        ax.plot(v['df_mse']['train'], color=color, linewidth=2.0, label=v['label'])

    setup_mse_axis(ax, mse_y_min, mse_y_max, MSE_LOG_SCALE)
    ax.set_title(f'Błąd MSE na zbiorze uczącym — {act_title}', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Epoka', fontsize=11)
    ax.set_ylabel('MSE' + (' (skala log.)' if MSE_LOG_SCALE else ''), fontsize=11)
    ax.legend(fontsize=10, framealpha=0.9)
    ax.set_xlim(left=0)
    plt.tight_layout()
    plt.savefig(f'{prefix}_wykres1_mse_train.png', dpi=SAVE_DPI, bbox_inches='tight')
    plt.close()

    # ------------------------------------------------------------------
    # Wykres 2: MSE — zbiór testowy + linia baseline
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=FIG_SIZE_MSE)
    for i, v in enumerate(variants_list):
        color = VARIANT_COLORS[i % len(VARIANT_COLORS)]
        ax.plot(v['df_mse']['test'], color=color, linewidth=2.0, label=v['label'])

    ax.axhline(y=baseline_mse, color='red', linestyle='--', linewidth=1.8,
               label=f'Surowe pomiary (MSE={baseline_mse:.4f})')
    setup_mse_axis(ax, mse_y_min, mse_y_max, MSE_LOG_SCALE)
    ax.set_title(f'Błąd MSE na zbiorze testowym — {act_title}', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Epoka', fontsize=11)
    ax.set_ylabel('MSE' + (' (skala log.)' if MSE_LOG_SCALE else ''), fontsize=11)
    ax.legend(fontsize=10, framealpha=0.9)
    ax.set_xlim(left=0)
    plt.tight_layout()
    plt.savefig(f'{prefix}_wykres2_mse_test.png', dpi=SAVE_DPI, bbox_inches='tight')
    plt.close()

    # ------------------------------------------------------------------
    # Wykres 3: CDF błędów pozycjonowania
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=FIG_SIZE_CDF)

    sorted_base = np.sort(baseline_errors)
    p_base = np.arange(1, len(sorted_base) + 1) / len(sorted_base)
    ax.plot(sorted_base, p_base, color='black', linestyle='--', linewidth=2.0, label='Surowe pomiary', zorder=3)

    for i, v in enumerate(variants_list):
        color = VARIANT_COLORS[i % len(VARIANT_COLORS)]
        sorted_err = np.sort(v['errors'])
        p = np.arange(1, len(sorted_err) + 1) / len(sorted_err)
        ax.plot(sorted_err, p, color=color, linewidth=2.0, label=v['label'], zorder=4)

    ax.set_xlim(0, cdf_xlim)
    ax.set_ylim(0, 1.02)
    ax.set_title(f'Dystrybuanta błędów pozycjonowania — {act_title}', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Błąd pozycjonowania [jednostki oryginalne]', fontsize=11)
    ax.set_ylabel('Prawdopodobieństwo (Dystrybuanta)', fontsize=11)
    ax.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.5)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    plt.tight_layout()
    plt.savefig(f'{prefix}_wykres3_cdf.png', dpi=SAVE_DPI, bbox_inches='tight')
    plt.close()

    # ------------------------------------------------------------------
    # Wykres 4: Scatter (TYLKO DLA NAJLEPSZEGO WARIANTU W GRUPIE)
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=FIG_SIZE_SCATTER)

    ax.scatter(measurements_test[:, 0], measurements_test[:, 1],
               c='#cccccc', s=12, alpha=0.70, zorder=1, label='Pomiary UWB (tło)')

    ax.scatter(best_variant['preds'][:, 0], best_variant['preds'][:, 1],
               c='#2980b9', s=16, alpha=0.85, zorder=2,
               label=f'Skorygowane (Najlepszy: {best_variant["label"]})')

    ax.scatter(real_test[:, 0], real_test[:, 1],
               c='#e74c3c', s=16, alpha=0.95, zorder=3, label='Wartości rzeczywiste (Ground Truth)')

    ax.set_title(f'Wyniki korekcji UWB — {act_title} (Zwycięzca: W{best_variant["variant"]})',
                 fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Współrzędna X [jednostki oryginalne]', fontsize=11)
    ax.set_ylabel('Współrzędna Y [jednostki oryginalne]', fontsize=11)
    ax.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.4)
    ax.legend(fontsize=10, framealpha=0.9, loc='best')
    ax.set_aspect('equal', adjustable='datalim')
    plt.tight_layout()
    plt.savefig(f'{prefix}_wykres4_scatter_best.png', dpi=SAVE_DPI, bbox_inches='tight')
    plt.close()

    return best_variant

# ==============================================================================
# START
# ==============================================================================

os.makedirs(PLOTS_DIR, exist_ok=True)

print("=" * 60)
print("Ładowanie danych i inicjalizacja skalerów...")

measurements_train_raw, real_train_raw = load_uwb_data(DATA_SOURCE_PATH, 'stat')
measurements_test_raw,  real_test_raw  = load_uwb_data(DATA_SOURCE_PATH, 'dyn')

measurements_train_raw = np.array(measurements_train_raw)
real_train_raw         = np.array(real_train_raw)
measurements_test_raw  = np.array(measurements_test_raw)
real_test_raw          = np.array(real_test_raw)

scaler_m, scaler_r = make_scalers(SCALER_TYPE)
scaler_m.fit(measurements_train_raw)
scaler_r.fit(real_train_raw)

meas_test_scaled = scaler_m.transform(measurements_test_raw)
real_test_scaled = scaler_r.transform(real_test_raw)

baseline_mse    = float(np.mean((meas_test_scaled - real_test_scaled) ** 2))
baseline_errors = euclidean_error(measurements_test_raw, real_test_raw)
cdf_xlim        = np.percentile(baseline_errors, CDF_PERCENTILE_ZOOM)

print(f"  Baseline MSE (znormalizowane): {baseline_mse:.6f}")
print(f"  Baseline mediana błędu:        {np.median(baseline_errors):.4f}")
print("=" * 60)

# ------------------------------------------------------------------------------
# Skanuj dostępne warianty pogrupowane po aktywacji
# ------------------------------------------------------------------------------
activation_groups = scan_variants(OUT_DIR)

if not activation_groups:
    raise RuntimeError(f"Nie znaleziono żadnych plików CSV w {OUT_DIR}!")

# ------------------------------------------------------------------------------
# Obliczanie wspólnej skali Y osi MSE dla WSZYSTKICH wariantów ze wszystkich grup
# ------------------------------------------------------------------------------
all_mse_values = [baseline_mse]
for act, v_list in activation_groups.items():
    for v in v_list:
        df = pd.read_csv(v['mse_path'], header=None, names=['train', 'test'])
        all_mse_values.extend(df['train'].tolist())
        all_mse_values.extend(df['test'].tolist())

mse_y_min = min(x for x in all_mse_values if x > 0) * 0.7
mse_y_max = MSE_YMAX if MSE_YMAX is not None else max(all_mse_values) * 1.5

# ------------------------------------------------------------------------------
# Generuj wykresy grupowe
# ------------------------------------------------------------------------------
print(f"\nZnaleziono grupy do przetworzenia: {list(activation_groups.keys())}")
print(f"Generuję wykresy z podziałem na grupy → {PLOTS_DIR}/")
print("-" * 60)

best_per_activation = {}

for act_name, v_list in activation_groups.items():
    print(f"\nPrzetwarzanie grupy: [{act_name.upper()}] (liczba wariantów: {len(v_list)})")

    best_v = plot_activation_group(
        act_name, v_list,
        measurements_test_raw, real_test_raw,
        baseline_mse, baseline_errors,
        mse_y_min, mse_y_max, cdf_xlim,
        PLOTS_DIR
    )

    best_per_activation[act_name] = best_v
    print(f"Wygenerowano 4 wykresy dla grupy {act_name}.")
    print(f"Najlepszy z grupy: W{best_v['variant']} (Mediana błedu: {best_v['median_err']:.4f})")

# ------------------------------------------------------------------------------
# Ranking końcowy (zestawienie najlepszych z najlepszych)
# ------------------------------------------------------------------------------
ranking = list(best_per_activation.values())
ranking.sort(key=lambda x: x['median_err'])

print("\n" + "=" * 60)
print("ZWYCIĘZCY Z POSZCZEGÓLNYCH FUNKCJI AKTYWACJI")
print("=" * 60)
medals = ["🥇", "🥈", "🥉"]
for rank, r in enumerate(ranking):
    medal = medals[rank] if rank < 3 else f"{rank+1:2d}."
    print(f"  {medal}  {r['activation'].capitalize():8s} - W{r['variant']:<10d}  "
          f"min_MSE={r['min_mse']:.6f}  "
          f"mediana_błędu={r['median_err']:.4f}")

print("=" * 60)
print(f"\nZakończono! Sprawdź folder: {PLOTS_DIR}/")