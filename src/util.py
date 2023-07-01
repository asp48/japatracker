import os


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def start_chrome_in_debug_mode(browser_app_path: str, port: int):
    if not is_port_in_use(port):
        os.system(
            f"nohup {browser_app_path} --remote-debugging-port={port} --user-data-dir='remote_debug_profile' &")
    else:
        print(f"Port {port} is in use.")