from mozart_argparser import MozartArgParser
from mozart_interpreter import MozartInterpreter


def main():
    arg_parser = MozartArgParser()
    args = arg_parser.parse()

    with open(args.filepath, "r", encoding="utf-8") as fp:
        code = fp.read()

    interpreter = MozartInterpreter()
    interpreter.run(code)


if __name__ == "__main__":
    main()
