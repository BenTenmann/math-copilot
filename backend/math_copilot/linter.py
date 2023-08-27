import logging
from typing import Final

import latex2sympy2
import sympy
from sympy.logic import boolalg as ba

from math_copilot import utils

LOGGER: Final[logging.Logger] = utils.get_logger(__name__)

BOOL_MAP: dict[ba.BooleanTrue | ba.BooleanFalse, bool] = {
    ba.BooleanFalse: False,
    ba.BooleanTrue: True,
}


def is_boolean(expression: sympy.Basic) -> bool:
    return isinstance(expression, (ba.BooleanTrue, ba.BooleanFalse))


def expression_to_bool(expression: ba.BooleanFalse | ba.BooleanTrue) -> bool:
    return BOOL_MAP[type(expression)]


def parse_latex_expression(latex_string: str) -> sympy.Basic:
    return latex2sympy2.latex2sympy(latex_string)


def expression_is_correct(
    expression: sympy.Basic, symbols: dict[str, sympy.Symbol]
) -> bool:
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


def latex_expression_is_correct(
    latex_string: str, symbols: dict[str, sympy.Symbol]
) -> bool:
    try:
        expression = parse_latex_expression(latex_string)
    except Exception as e:
        LOGGER.exception("Error occurred while parsing the LaTeX string")
        LOGGER.error(str(e))
        # TODO: better catch parsing errors
        return True
    return expression_is_correct(expression, symbols)
