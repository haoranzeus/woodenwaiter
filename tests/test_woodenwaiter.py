from nose.tools import assert_equal
from nose.tools import assert_raises
from nose.tools import assert_true
from nose.tools import assert_false

from woodenwaiter.woodenwaiter import WoodenMenu
from woodenwaiter.woodenwaiter import WoodenWaiter
from woodenwaiter.woodenwaiter import WoodenCooker
from woodenwaiter.woodenwaiter import WoodenCustomer


class TestWoodenMenu:
    def setup(self):
        self.table = 'cmdb'
        self.dish = 'custom_sync'
        self.foods = {
            "action": "sync_custom_data",
            "paras": "some_paras"
        }
        # self.foods = json.dumps(foods)
        self.menu = WoodenMenu(
                table=self.table, dish=self.dish, foods=self.foods)

    def teardown(self):
        pass

    def test_get_menu(self):
        table_dish, foods = self.menu.get_menu()
        assert_equal(table_dish, "cmdb:custom_sync")
        assert_equal(foods, self.foods)


class TestWoodenWaiter:
    def setup(self):
        self.waiter = WoodenWaiter()

    def teardown(self):
        pass

    def test_take_serve(self):
        table_dish = "cmdb:test_take_seve"
        foods = {
            "action": "sync_custom_data",
            "paras": "some_paras"
        }
        self.waiter.take_dish(table_dish, foods)
        get_foods = self.waiter.serve_dish(table_dish)
        assert_equal(foods, get_foods)
        assert_true(isinstance(get_foods, dict))


class TestWoodenCooker:
    def setup(self):
        self.table = 'cmdb'
        self.dish = 'custom_sync'
        self.foods = {
            "action": "sync_custom_data",
            "paras": "some_paras"
        }
        self.waiter = WoodenWaiter()
        self.menu = WoodenMenu(
                table=self.table, dish=self.dish, foods=self.foods)
        self.cooker = WoodenCooker(menu=self.menu, waiter=self.waiter)

    def teardown(self):
        pass

    def test_cookone(self):
        with assert_raises(AssertionError):
            self.cooker.cookone('not a WoodenMenu')

        self.cooker.cookone()
        get_foods = self.waiter.serve_dish(self.table+":"+self.dish)
        assert_equal(get_foods, self.foods)


class TestWoodenCustomer:
    def setup(self):
        self.table = 'cmdb'
        self.dish = 'test_customer'
        self.foods = {
            "action": "test_customer",
            "paras": "some_paras"
        }
        self.waiter = WoodenWaiter()
        self.menu = WoodenMenu(
                table=self.table, dish=self.dish, foods=self.foods)
        self.cooker = WoodenCooker(menu=self.menu, waiter=self.waiter)

        def processfoods(foods):
            return foods
        self.customer = WoodenCustomer(
                table=self.table, dish=self.dish,
                waiter=self.waiter, process=processfoods,
                seconds=10)

    def teardown(self):
        pass

    def test_call_waiter(self):
        assert_false(self.customer.call_waiter())   # 此时redis没有东西
        self.cooker.cookone()       # 塞入redis一个东西
        assert_equal(self.foods, self.customer.call_waiter())   # 进行相应处理
