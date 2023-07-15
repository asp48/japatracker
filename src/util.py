import glob
import os
from datetime import datetime
from typing import List, Any, Dict

from src import constants
from src.configs import env


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def start_chrome_in_debug_mode(browser_app_path: str, port: int):
    if not is_port_in_use(port):
        os.system(
            f"nohup {browser_app_path} --remote-debugging-port={port} --user-data-dir='/tmp/remote_debug_profile' &")
    else:
        print(f"Port {port} is in use.")


def get_unique_file_name(prefix: str):
    timestamp = datetime.now().strftime(constants.FILE_DATE_TIME_FORMAT)
    return prefix + "_" + timestamp


def write_list_to_local_output_file(prefix: str, data: List[List[Any]], headers: List[str]):
    data_str = "\n".join([",".join([str(item) for item in entry]) for entry in [headers] + data]) + "\n"
    write_str_to_local_output_file(prefix, data_str, "csv")


def write_str_to_local_output_file(prefix: str, data: str, extension: str, unique=True):
    if unique:
        file_path = f"{env.output_dir}/{prefix}/{get_unique_file_name(prefix)}.{extension}"
    else:
        file_path = f"{env.output_dir}/{prefix}.{extension}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+") as file:
        file.write(data)


def read_from_local_output_file(file_name: str, extension: str) -> str:
    file_path = f"{env.output_dir}/{file_name}.{extension}"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    else:
        return ""


def fetch_metrics_from_previous_run(keys: str) -> Dict[str, Any]:
    search_pattern = os.path.join(env.output_dir + "/" + constants.RAW_METRICS_PREFIX,
                                  constants.RAW_METRICS_PREFIX + '*.csv')
    matching_files = sorted(glob.glob(search_pattern), key=os.path.getmtime, reverse=True)
    result = {}
    if matching_files:
        with open(matching_files[0], "r") as f:
            for line in f.readlines():
                tokens = line.strip("\n").split(",")
                key, value = tokens[0], tokens[1]
                if key in keys:
                    result[key] = value
    return result


def get_deviation_percentage(current_count: int):
    start_date = datetime.strptime(constants.JAPA_YAGA_START_DATE, '%d-%m-%Y').date()
    diff_from_cur = (datetime.now().date() - start_date).days
    expected_japa_count = (diff_from_cur * constants.JAPA_YAGA_TARGET_COUNT) / constants.JAPA_YAGA_DURATION
    deviation = (current_count - expected_japa_count) * 100.0 / constants.JAPA_YAGA_TARGET_COUNT
    return format(deviation, ".2f")


def get_file_extension(file_name: str) -> str:
    tokens = file_name.split(".")
    return tokens[1] if len(tokens) > 0 else ""
