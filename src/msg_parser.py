from typing import List

from src.models.japa_entry import JapaEntry
from src.models.message import Message


def get_japa_entries(messages: List[Message]) -> List[JapaEntry]:
    japa_entries = []
    for message in messages:
        tokens = message.content.split(",")
        contributor = tokens[0].strip(" ")
        japa_count = int(tokens[1].strip("\n").strip(" "))
        japa_entry = JapaEntry(message.timestamp_str, contributor, japa_count)
        japa_entries.append(japa_entry)
    return japa_entries
