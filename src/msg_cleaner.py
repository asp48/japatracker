import re
from typing import List

from src import constants, util
from src.clients import spreadsheet_client
from src.models.message import Message

INVALID_MSG_LOG_HEADERS = ["timestamp", "sender", "content"]


def clean_messages(messages: List[Message], raw_sheet_id: str) -> List[Message]:
    valid_messages: List[Message] = []
    invalid_messages: List[Message] = []
    for msg in messages:
        if re.match(r'^\s*\([a-zA-Z .]{4,}\)\s*[0-9]+\s*$', msg.content):
            valid_messages.append(msg)
        else:
            invalid_messages.append(msg)
    log_invalid_messages(invalid_messages, raw_sheet_id)
    return valid_messages


def log_invalid_messages(messages: List[Message], raw_sheet_id: str):
    data = [[msg.timestamp_str, msg.sender, msg.content] for msg in messages]
    # write to local file
    util.write_list_to_local_output_file(constants.UNPROCESSED_SUB_SHEET, data, INVALID_MSG_LOG_HEADERS)
    # write to raw sheet on gdrive
    spreadsheet_client.write_new_sub_sheet(raw_sheet_id, constants.UNPROCESSED_SUB_SHEET, data, INVALID_MSG_LOG_HEADERS)
