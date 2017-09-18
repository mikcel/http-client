import socket


class SocketClient(object):
    def __init__(self, host, port=80, timeout=2):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.last_send_command = ""

        self.connect_socket()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect_socket(self):
        try:
            self.socket.connect((self.host, self.port))
        except socket.timeout:
            print("Socket connection timed out")
        except InterruptedError:
            print("Socket connection has been interrupted by a signal")

    def close_connection(self):
        if self.socket:
            self.socket.close()

    def send_cmd(self, method, doc_path, query="", params="", http_version="1.0"):

        if type(method) is not str or method.upper() not in ("GET", "POST"):
            print("Invalid method for library. Only GET and POST accepted.")
            return False
        elif type(doc_path) is not str:
            print("Document path is not of the correct data type. String expected")
            return False

        try:
            float(http_version)
        except ValueError:
            print("Incorrect HTTP Version.")
            return False

        complete_uri = "%s?%s" % (doc_path, query)

        self.last_send_command = "%s %s HTTP/%s" \
                                 "\r\nHost:%s" \
                                 "\r\n\r\n" % (method, complete_uri, str(http_version), self.host)

        print("======== REQUEST ========")
        print(self.last_send_command)

        self.socket.sendall(self.last_send_command.encode("utf-8"))

        return True

    def get_server_response(self):

        response = []
        while True:

            try:
                returned_data = self.socket.recv(len(self.last_send_command), socket.MSG_WAITALL)
            except socket.timeout:
                print("Unable to read response from host. Timed out.")
                return None

            if not returned_data:
                break
            else:
                response.append(returned_data.decode("utf-8"))

        return ''.join(response)
