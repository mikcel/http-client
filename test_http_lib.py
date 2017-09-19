import http_lib

if __name__ == "__main__":

    print("\r\n===GET REQUEST===")

    get_headers = {"Content-Type": "application/json", "Content-Length": 17}
    get_response = http_lib.get("http://httpbin.org/get?course=networking&assignment=1", headers=get_headers)

    if get_response:
        print("===GET RESPONSE===")
        print(get_response.status)
        print(get_response.get_headers_str())
        print(get_response.body)

    print("\r\n\r\n===POST REQUEST===")

    params = '{"Assignment": 1}'
    post_headers = {"Content-Type": "application/json", "Content-Length": len(params)}
    post_response = http_lib.post("http://httpbin.org/post", headers=post_headers, params=params)

    if post_response:
        print(post_response.status)
        print(post_response.get_headers_str())
        print(post_response.body)
