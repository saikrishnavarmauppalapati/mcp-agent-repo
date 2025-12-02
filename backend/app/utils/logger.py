import logging
import sys

def setup_logger(name: str = "mcp-agent", level: str = "INFO"):
    """
    Configure logging for the MCP agent backend.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # Formatter for logs
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Stream handler (prints logs to console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Avoid double-logging
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(stream_handler)

    return logger


# Global logger instance
logger = setup_logger()
