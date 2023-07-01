import configparser
import whatsapp_client
from src import msg_cleaner, msg_parser, sheets_exporter

config = configparser.ConfigParser()
config.read("configs/config.ini")

print("Reading messages from whatsapp...")
messages = whatsapp_client.get_msgs_from_browser(config["browser-config"]["browser"],
                                                 config["whatsapp-config"]["group_name"])
print(f"Messages Read: {len(messages)}")

print("Cleaning up invalid messages...")
messages = msg_cleaner.clean_messages(messages)
print(f"Messages post cleanup: {len(messages)}")

print("Parsing messages and creating entries...")
japa_entries = msg_parser.get_japa_entries(messages)
print(f"Entries post parsing: {len(japa_entries)}")

print("Exporting the entries to a sheet...")
sheets_exporter.export(japa_entries)

print("Tracking complete")
