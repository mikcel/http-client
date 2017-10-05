"""
test_http_lib.py
Script to test the HTTP Client library that uses TCP sockets. A GET and a POST request is made.
"""

__author__ = "Celine Mikiel Yohann"
__id__ = "40009948"

import sys
sys.path.append("../")
from httpc import http_lib

if __name__ == "__main__":

    print("\r\n===GET REQUEST===")

    get_headers = ["Content-Type:application/json"]
    get_response = http_lib.get("http://httpbin.org/get?course=networking&assignment=1", headers=get_headers)

    if get_response:
        print(get_response.status_code)
        print(get_response.get_headers_str())
        print(get_response.body)

    print("\r\n\r\n===POST REQUEST===")

    params = '{"Assignment": 1}'
    post_headers = ["Content-Type:application/json", "Content-Length:%s" % len(params)]
    post_response = http_lib.post("http://httpbin.org/post", headers=post_headers, params=params)

    if post_response:
        print(post_response.status_code)
        print(post_response.get_headers_str())
        print(post_response.body)

    print("\r\n===GET REQUEST (Redirect)===")

    get_headers = ["Content-Type:application/json"]
    get_response = http_lib.get("http://httpbin.org/redirect/3", headers=get_headers)

    if get_response:
        print(get_response.status_code)
        print(get_response.get_headers_str())
        print(get_response.body)
