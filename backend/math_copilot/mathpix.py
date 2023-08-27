import hashlib
import json
import os
import typing
from pathlib import Path

import requests

MATHPIX_APP_ID = os.environ.get("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.environ.get("MATHPIX_APP_KEY")
CACHE_DIR = Path(__file__).parent / "mathpix_cache"
CACHE_DIR.mkdir(exist_ok=True)

headers = {
    "app_id": MATHPIX_APP_ID,
    "app_key": MATHPIX_APP_KEY,
}


def image_to_latex(file_handle: typing.BinaryIO, logger=None) -> str:
    file_hash = hashlib.sha256(file_handle.read()).hexdigest()
    file_handle.seek(0)
    cache_file = CACHE_DIR / f"{file_hash}.json"
    if cache_file.exists():
        if logger:
            logger.info("Found in cache")
        with open(cache_file, "r") as f:
            result = json.load(f)
    else:
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
        with open(cache_file, "w") as f:
            json.dump(result, f)
    if logger:
        logger.info(result)
    return result["latex_styled"]


def split_latex_lines(x: str) -> list[str]:
    """Split a latex expression into lines"""
    x = x.replace("\\begin{aligned}\n", "")
    x = x.replace("\n\\end{aligned}", "")
    x = x.replace("\\\\\n", "\n")
    lines = x.split("\n")
    return [line.strip() for line in lines]
