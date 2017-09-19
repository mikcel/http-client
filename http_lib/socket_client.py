"""
socket_client.py
Script containing class for a Client Socket. The socket client obj will basically make a request to a host
by using info from an HTTP request obj defined in http_request.py. After making the request, an HTTP
Response is returned.
"""

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

import socket

from http_lib.http_request import HTTPRequest
from http_lib.http_response import HTTPResponse


class SocketClient(object):
    """
    Class representing a socket client. Need to initialize first with a request object and then send a
    request.
    """

    def __init__(self, request, timeout=2):

        if type(request) is not HTTPRequest:
            raise ValueError("Request obj is not correct")
        self.request = request

        # Initializes socket as TCP sockets and communicate with IPv4 sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(int(timeout))
        except ValueError:
            raise

        # Keep track of last sent request/command
        self.last_sent_request = ""

        self.connect_socket()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect_socket(self):
        """
        Method to connect to a socket on a host
        """
        try:
            self.socket.connect((self.request.host, self.request.port))
        except socket.gaierror:
            raise socket.gaierror("Socket connection could not be established")
        except socket.timeout:
            raise socket.timeout("Socket connection timed out")
        except InterruptedError:
            raise InterruptedError("Socket connection has been interrupted by a signal")

    def close_connection(self):
        """
        Method to close the socket connection.
        :return: None
        """
        if self.socket:
            self.socket.close()

    def send_request(self):

        """
        Method to send a request based on the request obj received
        :return: HTTPResponse object with server response info
        """

        # Get a formatted version of the request
        self.last_sent_request = self.request.format_request()

        # Send request in a byte-encoded format
        self.socket.sendall(self.last_sent_request.encode("utf-8"))

        # If POST method is made, params are also sent
        if self.request.method.upper() == "POST":
            self.socket.sendall(self.request.params.encode('utf-8'))

        return self.get_server_response()

    def get_server_response(self):

        """
        Method to read response from server after request has been sent.
        To ensure that reading is done correctly, a timeout has been set up.
        :return:
        """

        response = []
        while True:

            try:
                returned_data = self.socket.recv(len(self.last_sent_request), socket.MSG_WAITALL)
            except socket.timeout:
                print("Unable to read response from host. Timed out.")
                return None

            if not returned_data:
                break
            else:
                response.append(returned_data.decode("utf-8"))

        response_obj = HTTPResponse(''.join(response))
        return response_obj
