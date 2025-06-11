import socket


def check_connection(ip: str, port: int) -> bool:
    """Checks if a Service is Listening on the specified IP and Port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))

    return result == 0
