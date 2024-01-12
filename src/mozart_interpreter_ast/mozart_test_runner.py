import os
from pathlib import Path
from mozart_interpreter import MozartInterpreter
from mozart_ast import ValueType


class MozartTestRunner:
    def __init__(self, base_path: Path = Path("../../data/mozart_test_files/command_interpretation")):
        self.base_path = base_path

    def run(self):
        interpreter = MozartInterpreter()

        for filename in os.listdir(self.base_path):
            if filename.endswith(".mozart"):
                code_path = self.base_path.joinpath(Path(filename))
                with open(code_path, "r", encoding="utf-8") as fp:
                    code = fp.read()

                expected_final_state_path = self.base_path.joinpath(Path(filename.replace(".mozart", ".tmz")))
                with open(expected_final_state_path, "r", encoding="utf-8") as fp:
                    expected_final_state_txt = fp.read()
                    expected_final_state = eval(expected_final_state_txt)

                final_state = interpreter.run(code)

                assert final_state == expected_final_state


def main():
    MozartTestRunner().run()


if __name__ == "__main__":
    main()
