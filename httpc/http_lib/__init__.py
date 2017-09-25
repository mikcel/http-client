"""
Library main file. Contain get and post methods to make HTTP request using the HTTP Client library.
Both methods create a request object, make the resquest and return an HTTP response
"""

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

import time
from http_lib.socket_client import SocketClient
from httpc.http_lib.http_request import HTTPRequest


def get(url, headers=None):

    return __make_request(url=url, method="GET", headers=headers)


def post(url, params, headers=None):

    return __make_request(url=url, method="POST", headers=headers, params=params)


def __make_request(url, headers, method, params=None, max_redirect=4):

    redirect = True
    redirect_count = 1

    while redirect and redirect_count < max_redirect:

        # Create request from URL
        request = HTTPRequest(url=url, method=method, headers=headers, params=params)

        try:

            # Create client socket
            socket_clt = SocketClient(request)

            # Send the request and get a response
            response = socket_clt.send_request()

            socket_clt.close_connection()

        except Exception:
            raise

        if not response:
            print("Request not sent")
        else:
            if str(response.status_code).startswith("3"):
                new_location = response.headers.get("Location")
                if new_location:
                    if new_location.startswith("http"):
                        url = new_location
                    else:
                        url = "http://%s%s" % (request.host, new_location)
                    redirect_count += 1
                    print("Redirecting to: %s\r" % url)
                    time.sleep(2)
            else:
                return response

    return None
