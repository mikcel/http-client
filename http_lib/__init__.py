"""
Library main file. Contain get and post methods to make HTTP request using the HTTP Client library.
Both methods create a request object, make the resquest and return an HTTP response
"""

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

from http_lib.http_request import HTTPRequest
from http_lib.socket_client import SocketClient


def get(url, headers=None):
    # Create request from URL
    request = HTTPRequest(url=url, method="GET", headers=headers)

    # Create client socket
    socket_clt = SocketClient(request)

    # Send the request and get a response
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
