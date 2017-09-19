import re
from collections import OrderedDict


class HTTPResponse:
    def __init__(self, response_str):

        self.raw_response = response_str
        self.status = ""
        self.headers = OrderedDict()
        self.body = ""

        self.__parse_response()

    def __parse_response(self):

        split_response = self.raw_response.split("\r\n")

        try:

            self.status = split_response[0]

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

        headers_str = ""
        for key, value in self.headers.items():
            headers_str += "%s: %s\n" % (key, value)

        return headers_str
