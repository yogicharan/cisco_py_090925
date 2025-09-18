import logging
import json
import sys
from logging import Logger


class JSONFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
        }
        if record.exc_info:
            data["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(data)


def setup_logging(config):
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    if config.LOG_JSON:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.handlers = [handler]
