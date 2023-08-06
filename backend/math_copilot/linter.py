import sympy
import sympy.parsing.latex
from sympy.logic import boolalg as ba

BOOL_MAP: dict[
    ba.BooleanTrue | ba.BooleanFalse,
    bool
] = {
    ba.BooleanFalse: False,
    ba.BooleanTrue: True,
}


def is_boolean(expression: sympy.Basic) -> bool:
    return isinstance(expression, (ba.BooleanTrue, ba.BooleanFalse))


def expression_to_bool(expression: ba.BooleanFalse | ba.BooleanTrue) -> bool:
    return BOOL_MAP[type(expression)]


def expression_is_correct(latex_string: str, symbols: dict[str, sympy.Symbol]) -> bool:
    expression: sympy.Basic | ba.BooleanAtom | None = sympy.parsing.latex.parse_latex(latex_string)
    if expression is None:
        # the expression was not parsed
        return False
    if is_boolean(expression):
        # these are trivial cases
        return expression_to_bool(expression)

    substituted_expression = expression.subs(symbols)
    if is_boolean(substituted_expression):
        # with constraints imposed by the symbol definitions, the expression could be evaluated
        return expression_to_bool(substituted_expression)

    simplified_expression = sympy.simplify(substituted_expression)
    if is_boolean(simplified_expression):
        return expression_to_bool(simplified_expression)

    # otherwise, the expression is correct (*)
    # i.e. it is not possible to trivially show the expression is incorrect
    # TODO: see if there are better solvers out there
    return True
