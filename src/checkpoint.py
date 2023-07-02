from datetime import datetime
from typing import List

from src import util, constants
from src.models.message import Message


def record_check_point(messages: List[Message]):
    max_timestamp = int(max(messages, key=lambda obj: obj.timestamp).timestamp.timestamp())
    print(f"Recording max timestamp: {max_timestamp}")
    util.write_str_to_local_output_file(constants.CHECKPOINT_FILE_PREFIX, str(max_timestamp), "txt", False)


def get_checkpoint_timestamp():
    checkpoint_data = util.read_from_local_output_file(constants.CHECKPOINT_FILE_PREFIX, "txt")
    print(f"Timestamp read from checkpoint: {checkpoint_data}")
    if checkpoint_data == "":
        return None
    else:
        return datetime.fromtimestamp(int(checkpoint_data))
