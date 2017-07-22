# coding=utf-8
"""
synopsis: mock a customer that receive api by http
author: haoranzeus@gmail.com (zhanghaoran)
"""
import sys
import getopt
from bottle import post, request, run


@post('/api/customer1/')
def customer1():
    print('do some task here with the json received: {}'.format(request.json))
    return('ok')


def usage():
    print('usage: python3 takeout_customer.py '
          '[{-h, --host} <host>] [{-p, --port} <port>]\n')
    print('optional arguments:\n')
    print('  --help         show this help message and exit')
    print('  -h, --host     host to listen. default is localhost')
    print('  -p, --port     port to listen. default is 8080')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:p:", ["host=", "post=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit()

    host = 'localhost'
    port = 8080
    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('-h', '--host'):
            host = arg
        elif opt in ('-p', '--port'):
            port = str(arg)
        else:
            usage()
            exit()

    run(host=host, port=port, debug=True)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
