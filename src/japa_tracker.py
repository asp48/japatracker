import configparser

from clients import whatsapp_client
from src import msg_cleaner, msg_parser, entry_publisher, util, constants, report_generator, checkpoint
from src.clients import gclient

config = configparser.ConfigParser()
config.read("configs/config.ini")

print("Reading messages from whatsapp...")
all_messages = whatsapp_client.read_msgs(config["whatsapp-config"]["read_mode"],
                                         config["whatsapp-config"]["group_name"],
                                         config["browser-config"]["browser"],
                                         config["whatsapp-config"]["chats_file_path"],
                                         config["drive-config"]["input_folder_id"]
                                         )
print(f"Messages Read: {len(all_messages)}")

valid_messages = []
japa_entries = []

if len(all_messages) > 0:
    raw_sheet_id = gclient.create_new_spreadsheet(
        util.get_unique_file_name(constants.RAW_FILE_PREFIX),
        config["drive-config"]["folder_id"])

    print("Cleaning up invalid messages...")
    valid_messages = msg_cleaner.clean_messages(all_messages, raw_sheet_id)
    print(f"Messages post cleanup: {len(valid_messages)}")

    if len(valid_messages) > 0:
        print("Parsing messages and creating entries...")
        japa_entries = msg_parser.get_japa_entries(valid_messages)
        print(f"Entries post parsing: {len(japa_entries)}")

        print("Exporting the entries to a sheet...")
        entry_publisher.export(japa_entries,
                               config["drive-config"]["master_sheet_id"],
                               raw_sheet_id)

    checkpoint.record_check_point(all_messages)

metric_store = report_generator.capture_metrics(all_messages, valid_messages, japa_entries)
print(f"Metrics: \n {str(metric_store)}")
report_generator.save_metrics(metric_store)
print("Generating report...")
report_generator.generate_report(metric_store)

print("Tracking complete")
