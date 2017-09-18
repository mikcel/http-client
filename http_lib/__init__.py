from http_lib.socket_client import SocketClient
from urllib.parse import urlparse


def get(url):
    parsed_url = parse_url(url)
    if parsed_url is None:
        print("Request not sent")
        return

    netloc_info = parsed_url.netloc.split(":")
    host = netloc_info[0]
    try:
        port = netloc_info[1]
    except IndexError:
        port = 80

    socket_clt = SocketClient(host, port)

    request_sent = socket_clt.send_cmd("GET", parsed_url.path)
    if not request_sent:
        print("Request not sent")
    else:
        return socket_clt.get_server_response()


def parse_url(url):
    if url is None or len(url) == 0:
        print("Invalid URL")
        return None

    try:
        return urlparse(url, scheme="http")
    except ValueError:
        print("Invalid URL. Expected: scheme://host:port/path;parameters?query")
        return None
