import argparse


class MozartArgParser:
    def __init__(self):
        pass

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument("filepath", help="code file path in your SO.",
                            type=str)
        parser.add_argument("--show_final_state", help="code file path in your SO.",
                            type=bool, default=False)
        return parser.parse_args()
