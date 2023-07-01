import enum
from src.configs import env
import util

from selenium import webdriver


class BrowserType(enum.Enum):
    chrome = "chrome"


class Browser:

    def __init__(self, browser_type: BrowserType) -> None:
        if browser_type == browser_type.chrome:
            util.start_chrome_in_debug_mode(env.chrome_app_path, env.chrome_args["debug_port"])
            from selenium.webdriver.chrome.options import Options
            self.options: Options = Options()
            self.options.add_experimental_option("debuggerAddress", f"127.0.0.1:{env.chrome_args['debug_port']}")
            self.driver = webdriver.Chrome(executable_path=env.chrome_args["driver_path"], options=self.options)
            self.driver.implicitly_wait(env.implicit_wait_timeout)
        else:
            raise Exception(f"Unsupported browser type: {browser_type}")

    def open(self, url: str):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()
