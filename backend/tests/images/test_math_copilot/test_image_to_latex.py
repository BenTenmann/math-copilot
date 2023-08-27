from math_copilot.image_to_latex import image_to_latex


def test_zero_equals_one():
    with open("./tests/images/zero_equals_one.png", "rb") as f:
        latex = image_to_latex(f)
    assert latex == "0=1"


def test_two_x_squared_equals_4():
    with open("./tests/images/two_x_squared_equals_4.png", "rb") as f:
        latex = image_to_latex(f)
    assert (
        latex
        == "\\begin{aligned}\n2 x^{2} & =4 \\\\\nx^{2} & =2 \\\\\nx & = \\pm \\sqrt{2}\n\\end{aligned}"
    )
