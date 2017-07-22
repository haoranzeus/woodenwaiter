import time
from woodenwaiter.woodenwaiter import WoodenCustomer
from woodenwaiter.woodenwaiter import WoodenWaiter


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
        table=table, dish=dish,
        waiter=waiter, process=processfoods,
        seconds=1)

    customer.start()

    time.sleep(10)
    customer.terminate()


if __name__ == '__main__':
    test_wooden_customer()
