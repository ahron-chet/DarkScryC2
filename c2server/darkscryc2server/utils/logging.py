import atexit
import logging
import queue
from logging.handlers import QueueHandler, QueueListener
from typing import Optional

logger = logging.getLogger("darkscryc2server")

_listener: Optional[QueueListener] = None


def setup_logging(level: int = logging.INFO) -> None:
    """Configure asynchronous logging for the c2server only."""

    global _listener

    log_queue: queue.Queue[logging.LogRecord] = queue.Queue()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    queue_handler = QueueHandler(log_queue)

    logger.handlers.clear()
    logger.setLevel(level)
    logger.addHandler(queue_handler)

    _listener = QueueListener(log_queue, stream_handler)
    _listener.start()


def shutdown_logging() -> None:  # pragma: no cover - cleanup
    global _listener
    if _listener:
        _listener.stop()
        _listener = None


atexit.register(shutdown_logging)
