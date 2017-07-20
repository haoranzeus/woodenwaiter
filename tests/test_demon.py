from woodenwaiter.woodenwaiter import WoodenCustomer
from woodenwaiter.woodenwaiter import WoodenWaiter


def test_wooden_customer():
    """
    这个测试启动一个线程，可以通过命令行向redis的
    cmdb:test_customer_demon队列中塞入json数据，
    这面将打印出来
    """
    table = 'cmdb'
    dish = 'test_customer_demon'
    waiter = WoodenWaiter()

    def processfoods(foods):
        print(foods)

    customer = WoodenCustomer(
        table_dish=table+":"+dish,
        waiter=waiter, process=processfoods,
        seconds=1)

    customer.start()


if __name__ == '__main__':
    test_wooden_customer()
