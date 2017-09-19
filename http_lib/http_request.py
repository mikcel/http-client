import json
from urllib.parse import urlparse


class HTTPRequest:
    def __init__(self, url, method, headers=None, params=None):

        self.url = url
        self.method = method
        self.port = 80
        self.headers = headers
        self.params = params

        self.host = ""
        self.doc_path = ""
        self.query = ""

        self.__parse_request()

    def __parse_request(self):

        try:
            self.__validate_request()
        except ValueError:
            raise

        try:
            parsed_url = urlparse(self.url)
        except ValueError:
            raise ValueError("Invalid URL. Expected: scheme://host:port/path;parameters?query")

        netloc_info = parsed_url.netloc.split(":")
        self.host = netloc_info[0]
        try:
            self.port = netloc_info[1]
        except IndexError:
            self.port = 80

        self.doc_path = parsed_url.path
        self.query = parsed_url.query

    def __validate_request(self):

        if self.url is None or len(self.url) == 0:
            raise ValueError("Invalid URL")

        if not self.url.startswith("http") or self.url.startswith("https"):
            raise ValueError("Invalid URL. Only HTTP request.")

        if type(self.method) is not str or self.method.upper() not in ("GET", "POST"):
            raise ValueError("Invalid method for library. Only GET and POST accepted.")

        if self.headers is not None and type(self.headers) is not dict:
            raise ValueError("Incorrect data type for headers. Dict expected")

        if self.params is not None and type(self.params) is not str:
            raise ValueError("Incorrect data type for parameters. String expected")

    def format_request(self):

        complete_uri = self.doc_path
        if self.method.upper() == "GET":
            complete_uri = "%s?%s" % (self.doc_path, self.query)

        request_line = "%s %s HTTP/1.0" % (self.method, complete_uri)

        header_lines = "Host: %s\r\n" % self.host
        if self.headers is not None:
            for header, header_value in self.headers.items():
                header_lines += "%s: %s\r\n" % (header, header_value)

        formatted_request = "%s" \
                            "\r\n%s" \
                            "Connection: close\r\n" \
                            "\r\n" % (request_line, header_lines)

        return formatted_request
