from math_copilot.split_latex_lines import split_latex_lines


def test_zero_equals_one_lines_split():
    lines = split_latex_lines("0=1")
    assert lines == ["0=1"]


def test_two_x_squared_equals_4_split():
    lines = split_latex_lines(
        "\\begin{aligned}\n2 x^{2} & =4 \\\\\nx^{2} & =2 \\\\\nx & = \\pm \\sqrt{2}\n\\end{aligned}"
    )
    assert lines == ["2 x^{2} & =4", "x^{2} & =2", "x & = \\pm \\sqrt{2}"]
