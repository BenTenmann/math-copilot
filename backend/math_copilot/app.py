import io
import json
import os

import gradio as gr
import numpy as np
import requests
from dotenv import load_dotenv, find_dotenv
from PIL import Image

from math_copilot import linter

load_dotenv(find_dotenv())

MATHPIX_APP_ID: str = os.environ.get("MATHPIX_APP_ID")
MATHPIX_APP_KEY: str = os.environ.get("MATHPIX_APP_KEY")


def fn(img: np.ndarray) -> tuple[str, list[tuple[str, str]]]:
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
    is_correct = str(linter.expression_is_correct(latex_expression, {}))
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
