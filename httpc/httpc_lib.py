import argparse

from httpc import http_lib


def main():
    parent_parser = argparse.ArgumentParser(prog='httpc', add_help=False)

    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers()

    # HTTP GET Request subcommand
    parser_get = subparsers.add_parser('get', parents=[parent_parser], add_help=False)
    parser_get.set_defaults(func=get_request)
    parser_get.add_argument('url', metavar="URL")
    parser_get.add_argument('-v', dest="verbose", action="store_true")
    parser_get.add_argument('-h', dest="headers", type=str, metavar="key:value", action="append")

    # HTTP POST Request subcommand
    parser_post = subparsers.add_parser('post', parents=[parent_parser], add_help=False)

    parser_post.set_defaults(func=post_request)
    parser_post.add_argument('url', metavar="URL")
    parser_post.add_argument('-v', dest="verbose", action="store_true")
    parser_post.add_argument('-h', dest="headers", type=str, metavar="key:value", action="append")

    body_group = parser_post.add_mutually_exclusive_group()
    body_group.add_argument('-d', dest="data", type=str, metavar="string")
    body_group.add_argument('-f', dest="file", type=str, metavar="file")

    # Help subcommand
    help_parser = subparsers.add_parser('help', parents=[parent_parser], add_help=False)
    help_parser.set_defaults(func=show_help)
    help_parser.add_argument('command', nargs="*", type=str)

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        print("usage: httpc (help|get|post)")
        print("httpc Error: Missing subcommands")


def show_help(args):
    generic_help = """
    httpc is a curl-like application but supports HTTP protocol only.\r
    Usage: \r
    \thttpc command [arguments]\r
    The commands are: \r
    \tget executes a HTTP GET request and prints the response.\r
    \tpost executes a HTTP POST request and prints the response.\r 
    \thelp prints this screen.\r\n
    Use "httpc help [command]" for more information about a command.
    """

    get_request_help = """
    usage: httpc get [-v] [-h key:value] URL\r\n
    Get executes a HTTP GET request for a given URL.\r\n
    \t-v Prints the detail of the response such as protocol, status, and headers.\r
    \t-h key:value Associates headers to HTTP Request with the format 'key:value'.
    """

    post_request_help = """
    usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\r\n
    Post executes a HTTP POST request for a given URL with inline data or from file.\r\n
    \t-v Prints the detail of the response such as protocol, status, and headers.\r 
    \t-h key:value Associates headers to HTTP Request with the format 'key:value'.\r 
    \t-d string Associates an inline data to the body HTTP POST request.\r
    \t-f file Associates the content of a file to the body HTTP POST request.\r\n
    Either [-d] or [-f] can be used but not both.
    """
    help_usage = "usage: httpc help [get|post]"

    if args is None or not hasattr(args, "command"):
        print(help_usage)
        print("httpc Error: Error parsing subcommand")
    elif len(args.command) == 0:
        print(generic_help)
    elif len(args.command) == 1:
        if args.command[0] == "get":
            print(get_request_help)
        elif args.command[0] == "post":
            print(post_request_help)
        else:
            print(help_usage)
            print("httpc Error: Wrong subcommand for help. Try with 'get' or 'post'")
    elif len(args.command) > 1:
        print(help_usage)
        print("httpc Error: Only one subcommand is accepted for help. Try with 'get' or 'post'")


def get_request(args):
    try:

        url = args.url
        verbose = args.verbose
        headers = args.headers

        response = http_lib.get(url=url, headers=headers)
        if response:
            if verbose:
                print(response.status)
                print(response.get_headers_str())
            print(response.body)

    except AttributeError:
        print("usage: httpc get [-v] [-h key:value] URL")
        print("httpc Error: Arguments missing or not entered correctly'")


def post_request(args):
    try:

        url = args.url
        verbose = args.verbose
        headers = args.headers
        data = args.data
        file = args.file

    except AttributeError:
        print("usage: httpc get [-v] [-h key:value] URL")
        print("httpc Error: Arguments missing or not entered correctly'")

    else:

        correct_params = True
        params = ""
        if data is not None and file is None:
            params = data
        elif file is not None and data is None:
            try:
                with open(file, 'r') as data_file:
                    params = data_file.readlines()
            except (OSError, IOError):
                print("Unable to read data from file. Check file and try again")
                correct_params = False
        elif data is not None and file is not None:
            correct_params = False
            print("Cannot have inline data and file data at the same time")

        if correct_params:
            response = http_lib.post(url=url, headers=headers, params=params)
            if response:
                if verbose:
                    print(response.status)
                    print(response.get_headers_str())
                print(response.body)


if __name__ == "__main__":
    main()
