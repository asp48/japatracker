from typing import List

from src.models.japa_entry import JapaEntry
from src.models.message import Message


def get_japa_entries(messages: List[Message]) -> List[JapaEntry]:
    local_store = {}
    for message in messages:
        if message.date not in local_store:
            local_store[message.date] = {}
        tokens = message.content.split(",")
        contributor = tokens[0]
        japa_count = int(tokens[1])
        local_store[message.date][contributor] = local_store.get(message.date).get(contributor, 0) + japa_count
    japa_entries = []
    for date in local_store.keys():
        for contributor, japa_count in local_store[date].items():
            japa_entry = JapaEntry(date, contributor, japa_count)
            japa_entries.append(japa_entry)
    return japa_entries
