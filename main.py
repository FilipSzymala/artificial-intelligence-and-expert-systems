from util.parser import *

from util.program_modes import verify_all_mode, test_all_mode, default_mode

if __name__ == '__main__':
    args = parse_args()
    show_args(args)

    if args.mode == "test_all":
        test_all_mode(args)
    elif args.mode == "verify_all":
        verify_all_mode(args)
    else:
        default_mode(args)

