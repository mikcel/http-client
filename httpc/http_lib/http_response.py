"""
http_response.py
Script contains HTTPResponse class definition. This class represents an HTTP response.
"""

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

import re
from collections import OrderedDict


class HTTPResponse:
    """
    HTTP Response class that represents an HTTP response. It is initialize with a response string obtained
    after making an HTTP Request.
    """

    def __init__(self, response_str):

        """
        Constructor. Will initialize obj variable and get parse the response passed.
        :param response_str: Response string obtained after making an HTTP Request
        """

        self.raw_response = response_str
        self.status_line = ""
        self.status_code = ""
        self.status_code_desc = ""
        self.headers = OrderedDict()
        self.body = ""

        self.__parse_response()

    def __parse_response(self):

        """
        Method to parse/split the response string
        :return: None
        """

        split_response = self.raw_response.split("\r\n")

        try:

            # Split the status line to get status code and description
            self.status_line = split_response[0]
            status_line_regexp = re.compile("HTTP\/\d\.\d\s((?P<code>\d{3})\s(?P<desc>.*))", re.IGNORECASE)
            status_split = re.match(status_line_regexp, self.status_line)
            if status_split is not None and len(status_split.groupdict()) == 2:
                self.status_code = int(status_split.groupdict().get("code"))
                self.status_code_desc = status_split.groupdict().get("desc")

            # Get all headers until a return line feed is reached
            list_idx = 1
            while list_idx < len(split_response) and split_response[list_idx] != "":
                split_header = re.search(r'^(?P<key>.*):\s(?P<value>.*)$', split_response[list_idx].strip()).groupdict()
                self.headers.update({split_header["key"]: split_header["value"]})
                list_idx += 1

            if list_idx != len(split_response):
                self.body = split_response[list_idx + 1]

        except Exception as e:
            print(e)
            print("Unable to parse response. See raw response")

    def get_headers_str(self):

        """
        Method to obtain a string representation of the headers dict
        :return: String representing headers info
        """

        headers_str = ""
        for key, value in self.headers.items():
            headers_str += "%s: %s\n" % (key, value)

        return headers_str
