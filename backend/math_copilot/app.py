import base64
import io
import json
import logging
import os
from typing import Final

import pydantic

import fastapi
import requests
from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from math_copilot import linter, utils

load_dotenv(find_dotenv())

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


@app.post("/latex")
def image_to_latex(imgstr: str) -> Response:
    assert MATHPIX_APP_ID is not None
    assert MATHPIX_APP_KEY is not None
    pure_base64_str = imgstr.split(",")[1]
    imgdata = base64.b64decode(pure_base64_str)
    image = Image.open(io.BytesIO(imgdata))
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
    return Response(
        latex=latex_expression,
        is_correct=linter.latex_expression_is_correct(latex_expression, {})
    )
