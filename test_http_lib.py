import http_lib

if __name__ == "__main__":
    data = http_lib.get("http://httpbin.org/ip")
    print(data)
