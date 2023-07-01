import time
from typing import List

from src import constants
from src.configs import env
from src.models.message import Message


def clean_messages(messages: List[Message]) -> List[Message]:
    valid_messages: List[Message] = []
    invalid_messages: List[Message] = []
    for msg in messages:
        if msg.content.startswith(constants.VALID_MSG_PREFIX) and "," in msg.content:
            valid_messages.append(msg)
        else:
            invalid_messages.append(msg)
    log_invalid_messages(invalid_messages)
    return valid_messages


def log_invalid_messages(messages: List[Message]):
    cur_timestamp = str(time.time()).split(".")[0]
    with open(f"{env.output_dir}/invalid_messages-{cur_timestamp}.txt", "w+") as f:
        for msg in messages:
            f.write(str(msg) + "\n")
