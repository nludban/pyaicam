import socket


def local_ipaddr():
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        pass
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # RFC2544 - reserved test subnet 192.18/15
        sock.connect(( '192.18.0.1', 42 ))
        host, port = sock.getsockname()
        return host
    except:
        return '127.0.0.1'

#--#
