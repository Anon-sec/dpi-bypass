import socket
import signal
import sys

from config import PROXY_IP, PROXY_PORT, SOCKET_TIMEOUT
from proxy import handle_connection


# shared flag so threads know when to stop
run_flag = {"running": True}


def stop_proxy(sig, frame):
    print("\nStopping proxy...")
    run_flag["running"] = False


signal.signal(signal.SIGINT, stop_proxy)


def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((PROXY_IP, PROXY_PORT))
    server.listen(100)
    server.settimeout(SOCKET_TIMEOUT)

    print(f"Proxy running on {PROXY_IP}:{PROXY_PORT}")
    print("Press Ctrl + C to stop")

    try:
        while run_flag["running"]:
            try:
                client, _ = server.accept()
                handle_connection(client, run_flag)
            except socket.timeout:
                continue
    finally:
        server.close()
        print("Proxy stopped.")
        sys.exit(0)


if __name__ == "__main__":
    start_proxy()
