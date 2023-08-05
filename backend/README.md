# math-copilot: backend

## Setup

To setup the environment, run:

```bash
poetry install --no-root
```

If you do not have `poetry` installed, please refer to the [Poetry website](https://python-poetry.org/docs/#installation).

## Usage

To run the `gradio` app, run:

```bash
MATHPIX_APP_ID=... MATHPIX_APP_KEY=... poetry run python math_copilot/app.p
```

`MATHPIX_APP_ID` and `MATHPIX_APP_KEY` are secrets you will need to set.
