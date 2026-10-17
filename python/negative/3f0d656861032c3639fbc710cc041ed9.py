def connect_to_server_via_ssl_socket(host, port, timeout) -> socket.socket:
    """
    Connects to a server using a socket.

    Args:
        host (str): The server host to connect to.
        port (int): The port to connect to.
        timeout (int): The connection timeout in seconds.
    Returns:
        socket.socket: The connected socket object, or None if the connection failed.
    """
    import socket
    import ssl
    import time
    try:
        if port == 443:
            ssl_enable = True
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            server = socket.create_connection((host, port))
            ssl = context.wrap_socket(server, server_hostname=host)
            ssl.settimeout(timeout)
        else:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(timeout)
            server.connect((host, port))
        return server
    except socket.error as msg:
        print(f'Socket Error → {msg}')
        return None