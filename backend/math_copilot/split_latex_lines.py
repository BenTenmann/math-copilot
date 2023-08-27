def split_latex_lines(x: str) -> list[str]:
    x = x.replace("\\begin{aligned}\n", "")
    x = x.replace("\n\\end{aligned}", "")
    x = x.replace("\\\\\n", "\n")
    lines = x.split("\n")
    return [line.strip() for line in lines]
