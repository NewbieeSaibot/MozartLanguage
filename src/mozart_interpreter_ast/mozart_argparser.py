import argparse


class MozartArgParser:
    def __init__(self):
        pass

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument("filepath", help="code file path in your SO.",
                            type=str)
        return parser.parse_args()
