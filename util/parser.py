import argparse as ap

SOURCE_DIR_HELP="""Folder z pomiarami stat/dyn. 
DEFAULT='./resource/dane'


Wymagana struktura folderów z danymi:

dane
   |
   |--f8/
   |    |--dyn/
   |    |     f8_dyn_Xp
   |    |     f8_dyn_Xz
   |    |     ...
   |    |--stat/
   |          f8_stat_1
   |          f8_stat_2
   |          ...
   |--f10/
        |--dyn/
        |     f10_dyn_Xp
        |     f10_dyn_Xz
        |     ...
        |--stat/
              f10_stat_1
              f10_stat_2
              ...
   """

parser = ap.ArgumentParser(
    prog='sise_ex2',
    description='Solution for artificial intelligence and expert systems class.',
    epilog='\u00A9 2026 Program made by Filip Szymala & Filip Graczyk',
    formatter_class=ap.RawTextHelpFormatter
)


def parse_args():
    parser.add_argument(
        '-s', '--source',
        type=str,
        help=SOURCE_DIR_HELP,
        metavar="SOURCE_DIR",
        default='./resource/dane'
    )

    parser.add_argument(
        '-n', '--neurons',
        type=int,
        default=16,
        help='Liczba neuronów w warstwie ukrytej (DEFAULT=16)'
    )

    parser.add_argument(
        '-a', '--activation',
        default='relu',
        choices=['relu', 'logistic', 'tanh'],
        help='Funkcja aktywacji w warstwie ukrytej (DEFAULT=relu)'
    )

    parser.add_argument(
        '-lr', '--learning-rate',
        type=float,
        default=0.01,
        help='Współczynnik uczenia sieci (DEFAULT=0.01)'
    )

    parser.add_argument(
        '-o', '--optimizer',
        choices=['sgd', 'adam'],
        default='adam',
        help='Wybór algorytmu optymalizacji (DEFAULT=adam)'
    )

    parser.add_argument(
        '-b1', '--beta1',
        type=float,
        default=0.9,
        help='Współczynnik momentu dla SGD. Dla ADAM parametr beta1 (DEFAULT=0.9)'
    )

    parser.add_argument(
        '-b2', '--beta2',
        type=float,
        default=0.999,
        help='Beta 2 wykorzystywany jedynie dla algorytmu optymalizacji ADAM (DEFAULT=0.999)'
    )

    parser.add_argument(
        '-ep', '--epochs',
        type=int,
        default=50,
        help='Maksymalna liczba pełnych przejść przez cały zbiór treningowy (DEFAULT=50)'
    )

    parser.add_argument(
        '-r', '--runs',
        type=int,
        default=5,
        help='Liczba niezależnych prób uczenia sieci od zera (uśrednia wpływ losowych wag początkowych, DEFAULT=5)'
    )

    parser.add_argument(
        '-bs', '--batch-size',
        type=int,
        default=64,
        help='Rozmiar mini-wsadu danych. Zmniejszenie dodaje szum pomagający wyjść z minimów lokalnych (DEFAULT=64)'
    )

    parser.add_argument(
        '-sc', '--scaler',
        choices=['minmax', 'maxabs', 'standard'],
        default='minmax',
        help='Metoda normalizacji danych wejściowych (DEFAULT=minmax)'
    )

    return parser.parse_args()


def show_args(parsed_args: ap.Namespace, short=False):
    if short:
        print(parsed_args)
    else:
        print(f"Dane wejsciowe: '{parsed_args.source}'")
        print(f"Zastosowana funkcja normalizacji danych wejściowych: {parsed_args.scaler}")
        print(f"Liczba neuronow ukrytych sieci: {parsed_args.neurons}")
        print(f"Zastosowana funkcja aktywacji: {parsed_args.activation}")
        print(f"Współczynnik nauki sieci: {parsed_args.learning_rate}")
        print(f"Zastosowana funkcja optymalizacji sieci {parsed_args.optimizer}")
        print(f"Współczynniki beta1/momentum oraz beta2 (jeśli występuje): b1={parsed_args.beta1}, b2={parsed_args.beta2 or "brak"} ")
        print(f"Liczba epok w sieci: {parsed_args.epochs}")
        print(f"Wielkość pojedynczej partii przekazywanej na wejście sieci wybieranej w losowy sposób: {parsed_args.runs}")
