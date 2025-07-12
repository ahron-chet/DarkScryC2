import json
import atexit
import logging
import queue
from logging.handlers import QueueHandler, QueueListener
from typing import Optional

logger = logging.getLogger("darkscryc2server")

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            data["exc_info"] = self.formatException(record.exc_info)

        # Automatically include extra fields dynamically
        standard_attrs = logging.LogRecord(
            "", 0, "", 0, "", (), None
        ).__dict__
        for attr_name, attr_value in record.__dict__.items():
            if attr_name not in standard_attrs:
                data[attr_name] = attr_value

        return json.dumps(data)

_listener: Optional[QueueListener] = None

def setup_logging(level: int = logging.INFO) -> None:
    """Configure asynchronous JSON logging only for darkscryc2server."""

    global _listener

    log_queue: queue.Queue[logging.LogRecord] = queue.Queue()

    queue_handler = QueueHandler(log_queue)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.setLevel(level)
    logger.addHandler(queue_handler)

    _listener = QueueListener(log_queue, stream_handler)
    _listener.start()

def shutdown_logging() -> None:
    global _listener
    if _listener:
        _listener.stop()
        _listener = None

atexit.register(shutdown_logging)
