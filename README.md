# http-client

httpc is a Client Library to make HTTP GET/POST requests using TCP sockets. It allows features such as reading
data parameters from file and writing HTTP response to text files. More features are described below.

> Linux-Distribution only

## Features:

- GET Request
- POST Request
- Query Parameters
- Request Headers
- Request Body

## Getting Started

There are two ways to run the library, either using the python interpreter
or using the executable from a CLI.
<br>The Python script can be found under httpc directory "httpc_lib.py".
<br>The Linux executable can be found under httpc/dist "httpc"

### Commands

#### 1. Help commands

They basically show you a help message for each method and the general usage of the
library
```angular2html
./httpc help
./httpc help get
./httpc help post
```

#### 2. GET request

To perform a GET request, you can simply run the get command and pass a url to the executable/script
```angular2html
./httpc get "http://httpbin.org/get?test=httpc"
```

##### Options that you can use with GET command

| Option | Description |
| --- | --- |
| -v | **verbose**. In addition to printing the response body, the response headers are also retrieved |
| -h *key:value* | Used to associate headers to the request with the format 'key:value'. Can be use several times for more than one header |
| -o *file_name* | Writes the response body (and headers) to a file specified by *file_name*

#### 3. POST Request

This request method can be invoked by using the post command with the script or executable
```angular2html
httpc post -h Content-Type:application/json -d '{"Assignment": 1}' "http://httpbin.org/post"
```
##### Options that you can use with GET command

| Option | Description |
| --- | --- |
| -v | **verbose**. In addition to printing the response body, the response headers are also retrieved |
| -h *key:value* | Used to associate headers to the request with the format 'key:value'. Can be use several times for more than one header |
| -d *request_body* | Associates inline data to the body of the POST request |
| -f *file_name* | Associates the content of a file to the body of the POST request (relative path needed) |
| -o *file_name* | Writes the response body (and headers) to a file specified by *file_name*

> Either [-d] or [-f] can be used but not both.

## Additional Features

- Redirection capability

## Build With

- Python 3.5
- Socket built-in library
- PyInstaller (for the executable)

## Additional Notes

Lab Assignment for the Data Communication and Networking class
