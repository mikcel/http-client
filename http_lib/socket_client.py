import socket
from http_lib.http_response import HTTPResponse
from http_lib.http_request import HTTPRequest


class SocketClient(object):
    def __init__(self, request, timeout=2):

        if type(request) is not HTTPRequest:
            raise ValueError("Request obj is not correct")
        self.request = request

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(int(timeout))
        except ValueError:
            raise

        self.last_sent_command = ""

        self.connect_socket()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect_socket(self):
        try:
            self.socket.connect((self.request.host, self.request.port))
        except socket.gaierror:
            print("Socket connection could not be established")
        except socket.timeout:
            print("Socket connection timed out")
        except InterruptedError:
            print("Socket connection has been interrupted by a signal")

    def close_connection(self):
        if self.socket:
            self.socket.close()

    def send_request(self):

        self.last_sent_command = self.request.format_request()

        self.socket.sendall(self.last_sent_command.encode("utf-8"))

        if self.request.method.upper() == "POST":
            self.socket.sendall(self.request.params.encode('utf-8'))

        return self.get_server_response()

    def get_server_response(self):

        response = []
        while True:

            try:
                returned_data = self.socket.recv(len(self.last_sent_command), socket.MSG_WAITALL)
            except socket.timeout:
                print("Unable to read response from host. Timed out.")
                return None

            if not returned_data:
                break
            else:
                response.append(returned_data.decode("utf-8"))

        response_obj = HTTPResponse(''.join(response))
        return response_obj
