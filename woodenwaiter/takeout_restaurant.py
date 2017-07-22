# coding=utf-8
"""
synopsis: tekeout model. Do tasks by http API
author: haoranzeus@gmail.com (zhanghaoran)
"""
import json
import requests
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
