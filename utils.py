from datetime import datetime
from config import LOG_ENABLED


def write_log(text):
    if not LOG_ENABLED:
        return

    time_now = datetime.now().strftime("%H:%M:%S")
    print(f"[{time_now}] {text}")


def close_socket(sock):
    try:
        if sock:
            sock.close()
    except:
        pass
