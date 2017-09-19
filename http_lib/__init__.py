from http_lib.socket_client import SocketClient
from http_lib.http_request import HTTPRequest


def get(url, headers=None):
    request = HTTPRequest(url=url, method="GET", headers=headers)

    socket_clt = SocketClient(request)

    response = socket_clt.send_request()

    if not response:
        print("Request not sent")
    else:
        return response


def post(url, params, headers=None):
    request = HTTPRequest(url=url, method="POST", headers=headers, params=params)

    socket_clt = SocketClient(request)

    response = socket_clt.send_request()

    if not response:
        print("Request not sent")
    else:
        return response
