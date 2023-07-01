import time
from typing import List

import constants
from browser import Browser, BrowserType
from src.models.message import Message


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
            sender_details = msg_element.find_element_by_class_name("copyable-text").get_attribute("data-pre-plain-text")
            posted_time = sender_details.split(",")[0].strip("[")
            posted_date = sender_details.split("]")[0].split(",")[1].strip(" ")
            sender = sender_details.split("]")[1].strip(" ").strip(":")
            content = msg_element.find_element_by_class_name("selectable-text").text
            message = Message(posted_date, posted_time, sender, content)
            messages.append(message)
        except Exception as e:
            print(f"Could not process: {msg_element.text}, reason: {str(e)}")
    return messages




