from mozart_exceptions import *
from mozart_ast import ValueType


def belong(params, program_state):
    pass


def transpose(params, program_state):
    pass


def get(params, program_state):
    accepted_types = [ValueType.HARMONIC_FIELD, ValueType.CHORD, ValueType.NOTE, ValueType.SCALE]
    if len(params) != 2:
        raise WrongNumberOfParams(2, len(params))

    if not (params[0][0] in accepted_types):
        raise WrongParamType(accepted_types, params[0][0])

    if not (params[1][0] == ValueType.INTEGER):
        raise WrongParamType(ValueType.INTEGER, params[1][0])

    return params[0][1][params[1][1]]

def append_note(params, program_state):
    pass


def append_chord(params, program_state):
    pass
