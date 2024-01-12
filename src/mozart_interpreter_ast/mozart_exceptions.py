
class NotExistentVariableAttribution(Exception):
    def __init__(self, identifier: str):
        super().__init__(f"Semantic Error: Attribution of not existent variable '{identifier}'")


class WrongDomainVariableAttribution(Exception):
    def __init__(self, new_value_domain, real_domain):
        super().__init__(f"Semantic Error: new value domain is '{new_value_domain}',"
                         f" and the defined domain is '{real_domain}'")


class IdentifierAlreadyDefined(Exception):
    def __init__(self, identifier):
        super().__init__(
            f"Semantic Error: There is a variable already defined with the same identifier: '{identifier}'"
        )


class OperationBetweenDifferentDomain(Exception):
    def __init__(self, value_type_a, value_type_b):
        super().__init__(f"Wrong domain operation: '{value_type_a}', '{value_type_b}'")


class WrongDomainOperation(Exception):
    def __init__(self, value_type, defined_operation_domains):
        domains = ""
        for domain in defined_operation_domains:
            domains += domain + " "
        super().__init__(f"Wrong domain operation: '{value_type}', '{domains}'")


class ModuloZero(Exception):
    def __init__(self):
        pass


class WrongNumberOfParams(Exception):
    def __init__(self, expected_no_params, receive_no_params):
        super().__init__(f"Wrong number of params. Expect: '{expected_no_params}'. Receive: '{receive_no_params}'")


class WrongParamType(Exception):
    def __init__(self, expected_param_type, receive_type_param):
        exp_params = "|"
        if isinstance(expected_param_type, list):
            for p in expected_param_type:
                exp_params += p.name + "|"
        else:
            exp_params = expected_param_type.name
        super().__init__(f"Wrong param type. Expect: '{exp_params}'. Receive: '{receive_type_param}'")
