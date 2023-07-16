import sys

from clients import whatsapp_client
from src import msg_cleaner, msg_parser, entry_publisher, util, constants, report_generator, checkpoint
from src.clients import gclient
from src import config_manager

args = sys.argv

if len(args) > 1:
    print(f"Overriding default config file with {args[1]}")
    config_manager = config_manager.get_instance(args[1])
else:
    print("Using default config file...")
    config_manager = config_manager.get_instance(args[1])

print("Reading messages from whatsapp...")
all_messages = whatsapp_client.read_msgs(config_manager)
print(f"Messages Read: {len(all_messages)}")

valid_messages = []
japa_entries = []

if len(all_messages) > 0:
    raw_sheet_id = gclient.create_new_spreadsheet(
        util.get_unique_file_name(constants.RAW_FILE_PREFIX),
        config_manager.get_drive_output_folder_id())

    print("Cleaning up invalid messages...")
    valid_messages = msg_cleaner.clean_messages(all_messages, raw_sheet_id)
    print(f"Messages post cleanup: {len(valid_messages)}")

    if len(valid_messages) > 0:
        print("Parsing messages and creating entries...")
        japa_entries = msg_parser.get_japa_entries(valid_messages)
        print(f"Entries post parsing: {len(japa_entries)}")

        print("Exporting the entries to a sheet...")
        entry_publisher.export(japa_entries, config_manager.get_drive_master_sheet_id(), raw_sheet_id)

    checkpoint.record_check_point(all_messages)

metric_store = report_generator.capture_metrics(all_messages, valid_messages, japa_entries)
print(f"Metrics: \n {str(metric_store)}")
report_generator.save_metrics(metric_store)
print("Generating report...")
report_generator.generate_report(metric_store)

print("Tracking complete")
