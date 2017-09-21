"""
http_request.py
Script containing HTTPRequest class. It represents a an HTTP request that will be sent to a server through
TCP sockets.
"""
import re

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

from urllib.parse import urlparse


class HTTPRequest:
    """
    Class representing an HTTP Request with the url, method, headers and params if necessary.
    """

    def __init__(self, url, method, headers=None, params=None):

        """
        Constructor. Takes a complete url, request method, headers and params if applicable.
        From these info, the parse_result method will be called to organize the info.
        :param url: Complete url to send request to
        :param method: Request method
        :param headers: Request headers
        :param params: Request parameters
        """

        self.url = url
        self.method = method
        self.port = 80  # Default port
        self.headers = headers
        self.params = params

        self.host = ""
        self.doc_path = ""
        self.query = ""

        self.__parse_request()

    def __parse_request(self):

        """
        Method to parse info to make a request. From the info obtained when constructing the object, some
        validations will be made, the URL will be parsed and the info to make an HTTP request will be
        organized.
        :return: None
        """

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
        if len(self.doc_path) == 0:
            self.doc_path = "/"

        self.query = parsed_url.query

        if self.method.upper() == "POST" and len(self.params) > 0:
            content_len_regexp = re.compile("content-length:\s?\d", re.IGNORECASE)
            # Check that content-length was added, if not add it automatically
            if self.headers is not None and len(list(filter(content_len_regexp.match, self.headers))) == 0:
                self.headers.append("Content-Length: %s" % len(self.params))
            elif self.headers is None:
                self.headers = ["Content-Length: %s" % len(self.params), "Content-Type:application/json"]

    def __validate_request(self):

        """
        Method to validate information initialized to make a request
        In case of error, an exception will be raised
        :return: None
        """

        if self.url is None or len(self.url) == 0:
            raise ValueError("Invalid URL")

        if not self.url.startswith("http") or self.url.startswith("https"):
            raise ValueError("Invalid URL. Only HTTP request.")

        if type(self.method) is not str or self.method.upper() not in ("GET", "POST"):
            raise ValueError("Invalid method for library. Only GET and POST accepted.")

        if self.headers is not None and type(self.headers) is not list:
            raise ValueError("Incorrect data type for headers. list expected")

        if self.params is not None and type(self.params) is not str:
            raise ValueError("Incorrect data type for parameters. String expected")

    def format_request(self):

        """
        Method to format the request in a specific string for sending using TCP sockets
        :return: String containing the formatted request
        """

        complete_uri = self.doc_path
        if self.method.upper() == "GET":
            complete_uri = "%s?%s" % (self.doc_path, self.query)

        # HTTP version 1.0 is used by default
        request_line = "%s %s HTTP/1.0" % (self.method, complete_uri)

        header_lines = "Host: %s\r\n" % self.host
        if self.headers is not None and len(self.headers) != 0:
            self.headers[-1] = "%s\r\n" % self.headers[-1]
            header_lines += '\r\n'.join(self.headers)

        formatted_request = "%s" \
                            "\r\n%s" \
                            "Connection: close\r\n\r\n" % (request_line, header_lines)

        return formatted_request
