from math_copilot.mathpix import image_to_latex, split_latex_lines
from pathlib import Path

equation_with_variable = Path('tests','images','equation_with_variables')
# "zero_equals_one.png"

def test_zero_equals_one():
    with open(Path(equation_with_variable, "zero_equals_one.png"), "rb") as f:
        latex = image_to_latex(f)
    assert latex == "0=1"


def test_zero_equals_one_lines_split():
    lines = split_latex_lines("0=1")
    assert lines == ["0=1"]

def test_two_x_squared_equals_4():
    with open(Path(equation_with_variable,"two_x_squared_equals_4.png"), "rb") as f:
        latex = image_to_latex(f)
    assert (
        latex
        == "\\begin{aligned}\n2 x^{2} & =4 \\\\\nx^{2} & =2 \\\\\nx & = \\pm \\sqrt{2}\n\\end{aligned}"
    )

def test_two_x_squared_equals_4_split():
    lines = split_latex_lines(
        "\\begin{aligned}\n2 x^{2} & =4 \\\\\nx^{2} & =2 \\\\\nx & = \\pm \\sqrt{2}\n\\end{aligned}"
    )
    assert lines == ["2 x^{2} & =4", "x^{2} & =2", "x & = \\pm \\sqrt{2}"]



equation_without_variable = Path('tests','images','equation_without_variables')

equation_without_variables_fn: dict[str,str|None] = dict(
    Addition_1='1+5=7',
    BODMASS_order_1='1+5 \\div 2=3',
    BODMASS_order_2='1+5 \\times 3=18',
    BODMASS_order_3='10-6 \\div 2=2',
    BODMASS_order_4='10-6 \\times 2=8',
    Brackets_1='(10-6) \\times 2=-2',
    Division_1='15 \\div 3=4',
    Fraction_1='\\frac{2}{3}+\\frac{3}{4}=\\frac{5}{7}',
    Fraction_2='\\frac{2}{3} \\div \\frac{4}{5}=\\frac{8}{15}',
    Fraction_3='6 \\div 7=5 / 6',
    Integer_Fraction_1='1+\\frac{1}{3}=\\frac{2}{3}',
    Integer_Fraction_2='\\frac{6}{6}=0',
    Integer_Fraction_3='\\frac{6}{3}=3',
    Multiplication_1='7 \\times 11=76',
    Negative_Unary='9+-3=12',
    Subtraction_1='9-6=4',              
)

def test_equation_without_variable():
    for key, val in equation_without_variables_fn.items():
        fn_path = Path(equation_without_variable, f"{key}.png")
        with open(fn_path, "rb") as f:
            latex = image_to_latex(f)
        assert latex == val
