import socket
import threading

from config import SOCKET_TIMEOUT, USE_DOH
from dpi import looks_like_tls_hello, split_tls_packet
from utils import close_socket
from doh import resolve_domain


def handle_connection(client_sock, run_flag):
    try:
        client_sock.settimeout(SOCKET_TIMEOUT)

        request = client_sock.recv(4096)
        if not request.startswith(b"CONNECT"):
            close_socket(client_sock)
            return

        target = request.split(b" ")[1].decode()
        host, port = target.split(":")
        port = int(port)

        # DNS resolution (Strict DoH)
        if USE_DOH:
            ip = resolve_domain(host)
            if not ip:
                close_socket(client_sock)
                return
        else:
            ip = host

        server_sock = socket.create_connection((ip, port))
        server_sock.settimeout(SOCKET_TIMEOUT)

        client_sock.sendall(
            b"HTTP/1.1 200 Connection Established\r\n\r\n"
        )

        threading.Thread(
            target=pipe_data,
            args=(client_sock, server_sock, True, run_flag),
            daemon=True
        ).start()

        threading.Thread(
            target=pipe_data,
            args=(server_sock, client_sock, False, run_flag),
            daemon=True
        ).start()

    except Exception:
        close_socket(client_sock)


def pipe_data(source, target, from_client, run_flag):
    first_chunk = True

    while run_flag["running"]:
        try:
            chunk = source.recv(4096)
            if not chunk:
                break

            if from_client and first_chunk and looks_like_tls_hello(chunk):
                first_chunk = False
                split_tls_packet(chunk, target)
            else:
                target.sendall(chunk)

        except socket.timeout:
            continue
        except Exception:
            break

    close_socket(source)
    close_socket(target)
