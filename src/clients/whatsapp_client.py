import os
import time
from datetime import datetime
from typing import List, Dict, Any

from whatstk import df_from_txt_whatsapp

from src import constants, checkpoint
from src.browser import Browser, BrowserType
from src.clients import gclient
from src.config_manager import ConfigManager
from src.models.message import Message


def read_msgs(config_manager: ConfigManager):
    read_mode = config_manager.get_whatsapp_read_mode()
    if read_mode == "browser":
        browser = config_manager.get_browser()
        group_name = config_manager.get_whatsapp_group_name()
        messages = get_msgs_from_browser(browser, group_name)
    elif read_mode == "local_file":
        messages = get_msgs_from_file(config_manager.get_whatsapp_input_file())
    elif read_mode == "drive_file":
        os.makedirs(config_manager.input_dir, exist_ok=True)
        drive_folder_id = config_manager.get_drive_input_folder_id()
        file_path = gclient.load_latest_file_from_drive(drive_folder_id, config_manager.input_dir)
        messages = get_msgs_from_file(file_path) if file_path is not None else []
    else:
        raise Exception("Unsupported read mode")
    return get_messages_from_checkpoint(messages)


def get_messages_from_checkpoint(messages: List[Message]):
    chk_timestamp = checkpoint.get_checkpoint_timestamp()
    if not chk_timestamp:
        return messages
    print("Filtering out messages based on checkpoint...")
    filtered_msgs = [msg for msg in messages if msg.timestamp > chk_timestamp]
    print(f"Filtered messages count: {len(messages) - len(filtered_msgs)}")
    return filtered_msgs


def get_msgs_from_browser(browser: str, group_name: str) -> List[Message]:
    browser = Browser(BrowserType(browser))
    browser.open(constants.WHATSAPP_WEB_URL)
    time.sleep(5)
    browser.driver.find_element_by_xpath(
        f"{constants.CHATS_SELECT_PATH}//span[@title='{group_name}']"
    ).click()
    time.sleep(5)
    conversation_body_element = browser.driver.find_element_by_xpath(constants.CONVERSATION_MSGS_XPATH)
    msg_elements = conversation_body_element.find_elements_by_xpath(f".{constants.MSG_CONTAINER_XPATH}")
    messages: List[Message] = []
    for msg_element in msg_elements:
        try:
            sender_details = msg_element.find_element_by_class_name("copyable-text").get_attribute(
                "data-pre-plain-text")
            posted_timestamp = sender_details.split("]")[0].strip("[")
            sender = sender_details.split("]")[1].strip(" ").strip(":")
            content = msg_element.find_element_by_class_name("selectable-text").text
            datetime_obj = datetime.strptime(posted_timestamp, constants.WHATSAPP_TIMESTAMP_FORMAT)
            message = Message(datetime_obj, sender, content)
            messages.append(message)
        except Exception as e:
            print(f"Could not process: {msg_element.text}, reason: {str(e)}")
    browser.quit()
    return messages


def get_msgs_from_file(file_path: str) -> List[Message]:
    df = df_from_txt_whatsapp(file_path)
    messages = []
    for index, row in df.iterrows():
        messages.append(Message(row['date'].to_pydatetime(), row['username'], row['message']))
    return messages
