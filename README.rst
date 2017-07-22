WoodenWaiter
============
Python producer-customer model based on redis

Installment
-----------
use pip:

pip install woodenwaiter

from source code:

python3 setup.py install

Run Example
-----------
python3 -m woodenwaiter.woodenwaiter

Example Usage
-------------
A simple program that showing how to use WoodenWaiter
as a customer and producer

customer example:

.. code-block:: python

    import time

    from woodenwaiter.woodenwaiter import WoodenWaiter
    from woodenwaiter.woodenwaiter import WoodenCustomer
    from woodenwaiter.woodenwaiter import WoodenManager

    if __name__ == '__main__':
        table1 = 'cmdb'
        table2 = 'rbac'
        dish1 = 'custom_sync'
        dish2 = 'some_task'
        waiter = WoodenWaiter()

        def print_foods(foods):
            print('custom foods')
            print('foods is: {}'.format(foods))

        customer1 = WoodenCustomer(
                table=table1, dish=dish1, waiter=waiter,
                process=print_foods, seconds=1)
        customer2 = WoodenCustomer(
                table=table2, dish=dish2, waiter=waiter,
                process=print_foods, seconds=3)

        manager = WoodenManager()
        manager.add_customer(customer1)
        manager.add_customer(customer2)
        manager.launch()

        while True:
            time.sleep(1)

producer example:

.. code-block:: python

    import time
    import random

    from woodenwaiter.woodenwaiter import WoodenMenu
    from woodenwaiter.woodenwaiter import WoodenWaiter
    from woodenwaiter.woodenwaiter import WoodenCooker

    if __name__ == '__main__':
        table1 = 'cmdb'
        table2 = 'rbac'
        dish1 = 'custom_sync'
        dish2 = 'some_task'
        foods1 = {
            "action": "sync_custom_data",
            "paras": ""
        }
        foods2 = {
            "action": "some_action",
            "paras": {
                "para1": "value1",
                "para2": "value2"
            }
        }
        menu1 = WoodenMenu(table=table1, dish=dish1, foods=foods1)
        menu2 = WoodenMenu(table=table2, dish=dish2, foods=foods2)
        waiter = WoodenWaiter()
        cooker1 = WoodenCooker(menu=menu1, waiter=waiter)
        cooker2 = WoodenCooker(menu=menu2, waiter=waiter)

        cooker_running = True
        def cook_sometime():
            while cooker_running:
                seconds = random.randint(3, 10)
                time.sleep(seconds)
                print('cookone after {} seconds'.format(seconds))
                cooker1.cookone()
                cooker2.cookone()

        cooker_thread = threading.Thread(target=cook_sometime)
        cooker_thread.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                cooker_running = False
                manager.terminate_all()
                break

classes introduce
-----------------
Interoduce Classes of WoodenWaiter

WoodenMenu
~~~~~~~~~~
Each WoodenCooker cook **ONE** kind of food according to **ONE** WoodenMenu
instance. We create WoodenMenu instance by offer a table(maybe your program
model), a dish(maybe one kinds of your task) and foods(some informations
the customer need)

suggested format of parameter 'foods':

.. code-block:: python

    foods = {
        "action": "要执行的任务字符串",
        "paras": {"para1": "value1", "para2": "value2"}
    }

WoodenWaiter
~~~~~~~~~~~~
Each WoodenWater connect **ONE** redis database. We use WoodenWaiter to create
WoodenCooker instance and WoodenCustomer instance.

WoodenWater take dish from WoodenCooker(push task to redis list) and serve dish
to WoodenCustomer(pop task from redis).

WoodenCooker
~~~~~~~~~~~~
Creating an WoodenCooker need a WoodenMenu and a WoodenWaiter.

Methods:

set_menu(self, menu) - set WoodenMenu

set_waiter(self, waiter) - set WoodenWaiter

cookone(self, menu=None) - push a task to redis

WoodenCustomer
~~~~~~~~~~~~~~
WoodenCustomer take four parameters:

- table: maybe your program model
- dish: maybe one kind of your task
- waiter: a WoodenWaiter instance
- process: a function that accept a dictionary parameter. This function will be
  call when waiter serve a dish of food(when pop a task from redis).
- seconds: the seconds of the cycil that waiter check the redis.

WoodenCustomer is inherented from threading.Thread. But start the thread yourself
is not suggested. Please use WoodenManager instand.

Methods:

call_waiter(self) - call waiter to check if foods is OK(if there is a task in redis)

call_waiter_cyclic(self, seconds) - call waiter cyclic

terminate(self) - stop customer thread genteely

WoodenManager
~~~~~~~~~~~~~
WoodenManager is used for WoodenCustomer centralized management. We add woodenCustomer
instance to it, and then launch the threads

Methods:

add_customer(self, customer) - add WoodenCustomer instance

launch(self) - launch all WoodenCustomer Threads

terminate_all(self) - stop all customers thread genteely
