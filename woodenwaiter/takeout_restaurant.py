# coding=utf-8
"""
synopsis: tekeout model. Do tasks by http API
author: haoranzeus@gmail.com (zhanghaoran)
"""
import getopt
import json
import requests
import sys

from bottle import post, request, run

from .woodenwaiter import WoodenCustomer


class TakeoutCustomer(WoodenCustomer):
    """
    takeout customer
    Instand of do a python process when get a task, TakeoutCustomer call
    a RESTful-API.
    The method of the API is POST. The payload is the json formated stuff
    got from redis(the foods)

    paras:
        table - model name of the customer
        dish - some kind of task of the customer
        waiter - a WoodenWaiter instance
        customer_api_url - The RESTful-API url. We post foods to this url
        seconds - seconds that read redis cycle
    """
    def __init__(self, table, dish, waiter, customer_api_url, seconds):
        process = self.get_process_from_customer_api(customer_api_url)
        super(TakeoutCustomer, self).__init__(
                table, dish, waiter, process, seconds)

    @staticmethod
    def get_process_from_customer_api(customer_api_url):
        def process(foods):
            headers = {'content-type': 'application/json'}
            r = requests.post(customer_api_url, json.dumps(foods),
                              headers=headers)

        return process


@post('/woodenwaiter/takeout/add_cooker')
@post('/woodenwaiter/takeout/add_cooker/')
def add_cooker():
    """
    api for adding a cooker.
    payload:
        {
            "name": "cookername",
            "table": "modelname",
            "dish": "taskname",
            "foods": {
                "action": "something todo",
                "paras": "some paras"
            }
        }
    """
    menu_stuff = request.json
    try:
        cooker_name = menu_stuff['name']
        table = menu_stuff['table']
        dish = menu_stuff['dish']
        foods = menu_stuff['foods']
    except KeyError:
        # TODO(zhanghaoran) add some exception
        pass


def usage():
    banner = """
    __      _____   ___   __| | ___ _ __   __      ____ _(_) |_ ___ _ __ 
    \ \ /\ / / _ \ / _ \ / _` |/ _ \ '_ \  \ \ /\ / / _` | | __/ _ \ '__|
     \ V  V / (_) | (_) | (_| |  __/ | | |  \ V  V / (_| | | ||  __/ |   
      \_/\_/ \___/ \___/ \__,_|\___|_| |_|   \_/\_/ \__,_|_|\__\___|_|   

    """
    print(banner)
    print('usage: python -m woodenwaiter.takeout_restaurant '
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
    port = 8081
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
