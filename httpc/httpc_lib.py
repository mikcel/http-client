import argparse


def main():
    parent_parser = argparse.ArgumentParser(
        description='httpc is a curl-like application but supports HTTP protocol only',
        prog='httpc', add_help=False,
        usage='%(prog)s (help|get|post) [-v] [-h k:v]* [-d inline-data] [-f file] URL')

    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers()

    # HTTP GET Request subcommand
    parser_get = subparsers.add_parser('get', parents=[parent_parser], add_help=False)
    parser_get.set_defaults(func=get_request)
    parser_get.add_argument('url', metavar="URL", nargs=1)
    parser_get.add_argument('-v', dest="verbose", help="Prints the detail of the response such as protocol, status, "
                                                       "and headers.",
                            action="store_true")
    parser_get.add_argument('-h', dest="header", type=str, help="Associates headers to HTTP Request with the format "
                                                                "'key:value'.",
                            metavar="key:value", action="append")

    # HTTP POST Request subcommand
    parser_post = subparsers.add_parser('post', parents=[parent_parser], add_help=False)
    parser_post.set_defaults(func=post_request)
    parser_post.add_argument('url', metavar="URL", nargs=1)
    parser_post.add_argument('-v', dest="verbose", help="Prints the detail of the response such as protocol, status, "
                                                        "and headers.",
                             action="store_true")
    parser_post.add_argument('-h', dest="header", type=str, help="Associates headers to HTTP Request with the format "
                                                                 "'key:value'.",
                             metavar="key:value", action="append")
    body_group = parser_post.add_mutually_exclusive_group()
    body_group.add_argument('-d', dest="data", type=str, help="Associates an inline data to the body HTTP POST request.",
                            metavar="string")
    body_group.add_argument('-f', dest="file", type=str, help="Associates the content of a file to the body HTTP POST "
                                                              "request.",
                            metavar="file")

    # Help subcommand
    help_parser = subparsers.add_parser('help', parents=[parent_parser], add_help=False)
    help_parser.set_defaults(func=show_help)
    help_parser.add_argument('command', nargs=1, type=str, help='command')

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

    print(args)


def post_request(args):
    print(args)


if __name__ == "__main__":
    main()
