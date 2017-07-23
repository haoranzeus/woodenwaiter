# coding=utf-8
"""
synopsis: test demon
author: haoranzeus@gmail.com
"""
import time
import sys
from woodenwaiter.woodenwaiter import WoodenCustomer
from woodenwaiter.woodenwaiter import WoodenWaiter
from woodenwaiter.takeout_restaurant import TakeoutCustomer


def test_wooden_customer():
    """
    这个测试启动一个线程，可以通过命令行向redis的
    cmdb:test_customer_demon队列中塞入json数据，
    这面将其打印出来
    10秒钟后结束线程
    """
    table = 'cmdb'
    dish = 'test_customer_demon'
    waiter = WoodenWaiter()

    def processfoods(foods):
        print(foods)

    customer = WoodenCustomer(
        table=table, dish=dish, waiter=waiter, process=processfoods, seconds=1)

    customer.start()

    time.sleep(10)
    customer.terminate()


def test_takeout_customer():
    """
    Run takeout_customer.py before doing this test.
    This test will post foods to "http://localhost:8080/api/customer1/" when
    the customer get pop some stuff from  "cmdb:test_takeout_customer" list
    """
    table = 'cmdb'
    dish = 'test_takeout_customer'
    waiter = WoodenWaiter()
    url = 'http://localhost:8080/api/customer1/'

    customer = TakeoutCustomer(
        table=table, dish=dish, waiter=waiter, customer_api_url=url, seconds=2)

    customer.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            customer.terminate()
            sys.exit()


if __name__ == '__main__':
    """
    usage: python test_demon.py <name of test function>
    """
    exec(sys.argv[1] + '()')
