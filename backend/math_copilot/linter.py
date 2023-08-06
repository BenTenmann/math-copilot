import sympy
import sympy.parsing.latex


def evaluate_latex_expression(latex_string: str) -> bool:
    expression: sympy.Basic | bool = sympy.parsing.latex.parse_latex(latex_string)
    if isinstance(expression, bool):
        # these are trivial cases
        return expression

    if isinstance(expression, sympy.Equality):
        pass
