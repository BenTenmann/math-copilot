import json
import os
import typing

import requests

MATHPIX_APP_ID = os.environ.get("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.environ.get("MATHPIX_APP_KEY")


headers = {
    "app_id": MATHPIX_APP_ID,
    "app_key": MATHPIX_APP_KEY,
}


def image_to_latex(file_handle: typing.BinaryIO, logger=None) -> str:
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
        files={"file": file_handle},
        headers=headers,
    )
    response.raise_for_status()
    result = response.json()
    if logger:
        logger.info(result)
    return result["latex_styled"]
