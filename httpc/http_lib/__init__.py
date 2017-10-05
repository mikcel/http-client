"""
Library main file. Contain get and post methods to make HTTP request using the HTTP Client library.
Both methods create a request object, make the resquest and return an HTTP response
"""

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

import time
from httpc.http_lib.socket_client import SocketClient
from httpc.http_lib.http_request import HTTPRequest


def get(url, headers=None):
    """
    Method to perform a get request
    :param url: URL to get info from
    :param headers: Request headers as string
    :return: HTTPResponse object
    """

    return __make_request(url=url, method="GET", headers=headers)


def post(url, params, headers=None):
    """
    Method to perform a post request
    :param url: URL to get info from
    :param params: Params to post to url
    :param headers: Request headers as string
    :return: HTTPResponse object
    """

    return __make_request(url=url, method="POST", headers=headers, params=params)


def __make_request(url, headers, method, params=None, max_redirect=4):
    """
    Method to make an HTTP request given a method and url. Redirection is handled if needed. A count is
    kept for that purpose so as not to redirect indefinitely
    :param url: URL to make HTTP request to
    :param headers: Headers of the request
    :param method: Method of the request
    :param params: Params for POST request
    :param max_redirect: the maximum no. of redirections that can be made
    :return:
    """

    redirect = True
    redirect_count = 1

    # May be needed to redirect, a count is kept so as not to go to infinity
    while redirect and redirect_count <= max_redirect:

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
            # Check if redirection is needed
            if str(response.status_code).startswith("3"):
                new_location = response.headers.get("Location")
                if new_location:
                    if new_location.startswith("http"):
                        url = new_location
                    else:
                        url = "http://%s%s" % (request.host, new_location)

                    redirect_count += 1
                    print("Redirecting to: %s\r" % url)

                    # Sleep before redirection
                    time.sleep(2)
            else:
                return response

    print("Redirection tried but no results.")
    return None
