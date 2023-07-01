from typing import List


import time

from src.configs import env
from src.models.japa_entry import JapaEntry


def export(japa_entries: List[JapaEntry]):
    cur_timestamp = str(time.time()).split(".")[0]
    with open(f"{env.output_dir}/processed-{cur_timestamp}.csv", "w") as f:
        for entry in japa_entries:
            f.write(f"{entry.date},{entry.contributor},{entry.count}\n")