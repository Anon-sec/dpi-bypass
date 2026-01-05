import time
from config import TLS_DELAY_FIRST, TLS_DELAY_SECOND


def looks_like_tls_hello(packet):
    return packet.startswith(b"\x16\x03")


def split_tls_packet(packet, out_socket):
    # first small part (do not change size unless you know why)
    out_socket.sendall(packet[:5])
    time.sleep(TLS_DELAY_FIRST)

    # second part (safe to tweak delay only)
    out_socket.sendall(packet[5:20])
    time.sleep(TLS_DELAY_SECOND)

    # rest of the data
    out_socket.sendall(packet[20:])
