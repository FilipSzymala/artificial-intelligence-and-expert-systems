from util.parser import *

from util.program_modes import verify_all_mode, test_all_mode, default_mode, generate_charts_mode, \
    test_number_of_fails_mode

if __name__ == '__main__':
    args = parse_args()
    show_args(args)

    if args.mode == "test_all":
        test_all_mode()
    elif args.mode == "verify_all":
        verify_all_mode()
    elif args.mode == "generate_charts":
        generate_charts_mode()
    elif args.mode == "test_number_of_fails":
        test_number_of_fails_mode()
    else:
        default_mode(args)