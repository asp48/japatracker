from datetime import datetime

from src import constants


class Message:
    def __init__(self, timestamp: datetime, sender: str, content: str):
        self.timestamp = timestamp
        self.sender = sender
        self.content = content
        self.timestamp_str = self.timestamp.strftime(constants.MSG_DATE_TIME_FORMAT)

    def __str__(self):
        return f"[{self.timestamp_str}] {self.sender}: {self.content}"
