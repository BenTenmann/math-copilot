import io
import json
import logging
import os
from typing import Final
from math_copilot.LLM import LLM

import gradio as gr
import numpy as np
import requests
from dotenv import load_dotenv, find_dotenv
from PIL import Image

from math_copilot import linter, utils

load_dotenv(find_dotenv())

LOGGER: Final[logging.Logger] = utils.get_logger(__name__)

MATHPIX_APP_ID: Final[str | None] = os.environ.get("MATHPIX_APP_ID")
MATHPIX_APP_KEY: Final[str | None] = os.environ.get("MATHPIX_APP_KEY")


def fn(img: np.ndarray) -> tuple[str, list[tuple[str, str]]]:
    assert MATHPIX_APP_ID is not None
    assert MATHPIX_APP_KEY is not None

    image = Image.fromarray(img)
    filehandle = io.BytesIO()
    image.save(filehandle, "jpeg")
    filehandle.seek(0)
    headers = {
        "app_id": MATHPIX_APP_ID,
        "app_key": MATHPIX_APP_KEY,
    }
    response = requests.post(
        "https://api.mathpix.com/v3/text",
        data={
            "json_options": json.dumps(
                {
                    "rm_spaces": True,
                    "math_inline_delimiters": ["$", "$"],
                }
            )
        },
        files={"file": filehandle},
        headers=headers,
    )
    response.raise_for_status()
    latex_expression = response.json()["latex_styled"]
    isValid =linter.latex_expression_is_correct(latex_expression, {})
    if not isValid:
        llm = LLM()
        llm_response = llm.explain_error(latex_expression)
        print(llm_response)
    is_correct = str(isValid)
    if "$" not in latex_expression:
        latex_expression = f"$$\n{latex_expression}\n$$"
    return latex_expression, [(is_correct, is_correct)]


def main():
    gr.Interface(
        fn,
        inputs=gr.components.Image(
            shape=(224, 224),
            image_mode="L",
            invert_colors=False,
            source="canvas",
            tool="brush",
            brush_radius=10,
        ),
        outputs=[
            gr.Markdown(),
            gr.HighlightedText().style(color_map={"True": "green", "False": "red"})
        ],
        title="Math Copilot",
    ).launch()


if __name__ == "__main__":
    main()
