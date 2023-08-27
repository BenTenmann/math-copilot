import logging
from typing import Final


class ColorFormatter(logging.Formatter):
    """Logging formatter that adds colors to the log levels."""

    _colors: Final[dict[str, str]] = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[91m",
    }
    _reset: Final[str] = "\033[0m"

    def format(self, record):
        """Format the log record."""
        output = super(ColorFormatter, self).format(record)
        color = self._colors.get(record.levelname, "")
        if not color:
            return output
        return f"{color}{output}{self._reset}"


def get_logger(name: str) -> logging.Logger:
    """Get a logger with a given name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = ColorFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
