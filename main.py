from util.parser import *

from util.program_modes import default_mode

if __name__ == '__main__':
    args = parse_args()
    show_args(args)

    default_mode(args)