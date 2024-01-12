from mozart_argparser import MozartArgParser
from mozart_interpreter import MozartInterpreter
from pathlib import Path
import warnings


warnings.filterwarnings("ignore")


def main():
    arg_parser = MozartArgParser()
    args = arg_parser.parse()

    with open(Path(args.filepath), "r", encoding="utf-8") as fp:
        code = fp.read()

    interpreter = MozartInterpreter()
    final_state = interpreter.run(code)

    if args.show_final_state:
        print(final_state)


if __name__ == "__main__":
    main()
