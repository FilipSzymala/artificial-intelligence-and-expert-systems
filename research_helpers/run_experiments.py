import os
import subprocess

# Upewnijmy się, że folder na wyniki istnieje
os.makedirs('../out', exist_ok=True)

activations = ['relu', 'tanh', 'logistic']

# Dodano 5. "Zwycięski" wariant: precyzyjna pojemność, mniejszy krok, zero dropoutu
variants = [
    {'neurons': 16, 'lr': 0.01,  'batch_size': 64,  'dropout': 0.0},  # W1: Baza
    {'neurons': 32, 'lr': 0.005, 'batch_size': 32,  'dropout': 0.2},  # W2: Szersza, mały batch
    {'neurons': 64, 'lr': 0.001, 'batch_size': 128, 'dropout': 0.4},  # W3: Potężna pojemność
    {'neurons': 16, 'lr': 0.05,  'batch_size': 64,  'dropout': 0.1},  # W4: Szybki skok
    {'neurons': 32, 'lr': 0.005, 'batch_size': 64,  'dropout': 0.0},  # W5: Złoty środek (Precyzja)
]

# Zmienne stałe (żeby eksperyment był sprawiedliwy)
EPOCHS = 300
RUNS = 5
PATIENCE = 20

print(f"Rozpoczynam automatyczne zawody! Do przetestowania: {len(activations) * len(variants)} kombinacji.")
print("=" * 60)

for activation in activations:
    print(f"\n🏆 ROZPOCZYNAM LIGĘ: {activation.upper()} 🏆")
    print("-" * 40)

    for i, variant in enumerate(variants):
        base_name = f"{activation}_var{i + 1}"
        file_mse = f"./out/{base_name}_mse.csv"
        file_out = f"./out/{base_name}_output.csv"

        # INTELIGENTNY POMIJACZ (CACHE)
        # Jeśli oba pliki już istnieją w folderze ./out/, skrypt pomija ten wariant!
        if os.path.exists(file_mse) and os.path.exists(file_out):
            print(f"⏩ POMIJAM Wariant nr {i + 1} dla {activation} - wyniki już istnieją na dysku.")
            continue

        print(f"\nUruchamiam Wariant nr {i + 1} dla {activation}...")

        # Budowanie komendy tak, jakbyś ręcznie wpisywał ją w terminal
        command = [
            "python", "main.py",
            "-a", activation,
            "-n", str(variant['neurons']),
            "-lr", str(variant['lr']),
            "-o", "adam",
            "-bs", str(variant['batch_size']),
            "-dor", str(variant['dropout']),
            "-ep", str(EPOCHS),
            "-r", str(RUNS),
            "-p", str(PATIENCE)
        ]

        # Uruchomienie procesu uczenia
        subprocess.run(command)

        # Zmiana nazw plików wygenerowanych przez main.py, aby przypisać je do odpowiedniego wariantu
        if os.path.exists("./out/best_mse.csv"):
            os.rename("./out/best_mse.csv", file_mse)

        if os.path.exists("./out/best_output.csv"):
            os.rename("./out/best_output.csv", file_out)

        print(f"✅ Wariant {i + 1} zapisany pomyślnie jako: {base_name}_...csv")

print("\n" + "=" * 60)
print('🎉 Skrypt zakończono powodzeniem! Wszystkie brakujące warianty zostały doliczone.')