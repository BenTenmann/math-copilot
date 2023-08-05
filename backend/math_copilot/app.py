import io
import json
import os

import gradio as gr
import requests
from PIL import Image

MATHPIX_APP_ID: str = os.environ["MATHPIX_APP_ID"]
MATHPIX_APP_KEY: str = os.environ["MATHPIX_APP_KEY"]


def fn(img):
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
    return response.json()["latex_styled"]


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
        outputs="text",
        title="Math Copilot",
    ).launch()


if __name__ == "__main__":
    main()
