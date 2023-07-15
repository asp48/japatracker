from typing import List

from src import constants, util
from src.clients import gclient
from src.models.japa_entry import JapaEntry

DATA_HEADERS = ["date", "contributor", "count"]


def export(japa_entries: List[JapaEntry], master_sheet_id: str, raw_sheet_id: str):
    data = [[entry.date, entry.contributor, entry.count] for entry in japa_entries]
    # write to local file
    util.write_list_to_local_output_file(constants.PROCESSED_SUB_SHEET, data, DATA_HEADERS)
    # write to a raw sheet on gdrive
    gclient.write_new_sub_sheet(raw_sheet_id, constants.PROCESSED_SUB_SHEET, data, DATA_HEADERS)
    # append to master sheet on gdrive
    gclient.append_to_sheet(master_sheet_id, data, DATA_HEADERS)
