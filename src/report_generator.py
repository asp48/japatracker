from typing import Dict, Any, List

from src import util, constants
from src.models.japa_entry import JapaEntry
from src.models.message import Message

RAW_METRIC_FILE_HEADERS = ["Metric Name", "Value"]


def capture_metrics(all_msgs: List[Message], valid_msgs: List[Message], japa_entries: List[JapaEntry]) -> Dict[
    str, Any]:
    metric_store = {
        constants.MSG_READ_COUNT: len(all_msgs),
        constants.VALID_MSG_COUNT: len(valid_msgs),
        constants.JAPA_ENTRIES_COUNT: len(japa_entries),
        constants.UNIQUE_CONTRIBUTOR_COUNT: len(set([entry.contributor for entry in japa_entries])),
        constants.CURRENT_JAPA_COUNT: sum([entry.count for entry in japa_entries])
    }
    previous_metrics = util.fetch_metrics_from_previous_run(constants.TOTAL_JAPA_COUNT)
    metric_store[constants.TOTAL_JAPA_COUNT] = int(previous_metrics.get(constants.TOTAL_JAPA_COUNT, 0)) \
                                               + metric_store[constants.CURRENT_JAPA_COUNT]
    metric_store[constants.COMPLETION_PERCENTAGE] = format(
        metric_store[constants.TOTAL_JAPA_COUNT] * 100.0 / constants.JAPA_YAGA_TARGET_COUNT,
        ".2f")
    metric_store[constants.DEVIATION_PERCENTAGE] = util.get_deviation_percentage(
        metric_store[constants.TOTAL_JAPA_COUNT])
    return metric_store


def save_metrics(metrics_store: Dict[str, Any]):
    data = [[k, v] for k, v in metrics_store.items()]
    util.write_list_to_local_output_file(constants.RAW_METRICS_PREFIX, data, RAW_METRIC_FILE_HEADERS)


def generate_report(metrics_store: Dict[str, Any]):
    with open("resources/metrics_template.html", "r") as f:
        metrics_template = f.read()
    for key, value in metrics_store.items():
        metrics_template = metrics_template.replace("{{" + key + "}}", str(value))
    util.write_str_to_local_output_file(constants.METRICS_REPORT_PREFIX, metrics_template, "html")
