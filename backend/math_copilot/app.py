import base64
import io
import logging
import os
from typing import Final

import fastapi
import pydantic
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

import math_copilot.mathpix as mathpix
from math_copilot import linter, llm, utils

LOGGER: Final[logging.Logger] = utils.get_logger(__name__)

MATHPIX_APP_ID: Final[str | None] = os.environ.get("MATHPIX_APP_ID")
MATHPIX_APP_KEY: Final[str | None] = os.environ.get("MATHPIX_APP_KEY")

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Response(pydantic.BaseModel):
    latex: str
    is_correct: bool
    explanation: str


class Request(pydantic.BaseModel):
    image: str


def rgba_to_rgb(image, color=(255, 255, 255)):
    """Convert an RGBA image to RGB format.

    Args:
        image: PIL.Image object with 4 channels.
        color: Tuple representing the RGB values of the background color. Default is white.

    Returns:
        PIL.Image object with 3 channels.
    """
    alpha = image.split()[3]
    bg = Image.new("RGB", image.size, color)
    bg.paste(image, mask=alpha)
    return bg


@app.post("/latex")
def image_to_latex(r: Request) -> Response:
    assert MATHPIX_APP_ID is not None
    assert MATHPIX_APP_KEY is not None
    imgstr = r.image
    pure_base64_str = imgstr.split(",")[1]
    imgdata = base64.b64decode(pure_base64_str)
    image = Image.open(io.BytesIO(imgdata))
    filehandle = io.BytesIO()
    image = rgba_to_rgb(image)
    image.save(filehandle, "jpeg")
    filehandle.seek(0)
    latex_expression = mathpix.image_to_latex(filehandle, logger=LOGGER)
    lines_of_latex = mathpix.split_latex_lines(latex_expression)
    lines_of_latex_are_valid = []
    for latex_expression in lines_of_latex:
        lines_of_latex_are_valid.append(
            linter.latex_expression_is_correct(latex_expression, {})
        )
    if not all(lines_of_latex_are_valid):
        resp = llm.explain_error(lines_of_latex)
    else:
        resp = ""
    return Response(
        latex=latex_expression, is_correct=all(lines_of_latex_are_valid), explanation=resp
    )


@app.post("/explain/error")
def explain_error(latex: str) -> str:
    """Explain the error in a problem

    Args:
        latex (str): the latex expression

    Returns:
        str: explanation of error
    """
    resp = llm.explain_error(latex)
    return resp


@app.post("/explain/solution")
def explain_solution(latex: str) -> str:
    """Explain the solution to a problem

    Args:
        latex (str): the latex expression

    Returns:
        str: explanation of solution
    """
    resp = llm.explain_solution(latex)
    return resp
