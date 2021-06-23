# Author: Alan Tort
# Date: 6/22/2021
# Description: Unit testing for Store.py

import unittest
from Store import Product
from Store import Customer
from Store import Store
from Store import InvalidCheckoutError


class test_store(unittest.TestCase):

    def test_product(self):
        """Testing the methods of the Product class"""
        new_product = Product(926, "checkers", "game", 50, 5)
        product_id = new_product.get_product_id()
        product_title = new_product.get_title()
        product_description = new_product.get_description()
        product_price = new_product.get_price()
        product_availability = new_product.get_quantity_available()
        self.assertEqual(product_id, 926)
        self.assertEqual(product_title, "checkers")
        self.assertEqual(product_description, "game")
        self.assertEqual(product_price, 50)
        self.assertEqual(product_availability, 5)

    def test_customer(self):
        """Testing the methods of the Customer class"""
        new_customer = Customer("Alan", "ABC", True)
        customer_name = new_customer.get_name()
        customer_id = new_customer.get_customer_id()
        premium_member = new_customer.is_premium_member()
        self.assertNotEqual(customer_name, "Eric")
        self.assertNotEqual(customer_id, "DEF")
        self.assertNotEqual(premium_member, False)
        self.assertTrue(premium_member, True)

    def test_store(self):
        """Testing a general implementation of all Store.py classes and methods"""
        checkers = Product(926, "checkers", "game", 50, 5)
        chess = Product(641, "chess", "game", 25, 1)
        customer1 = Customer("Alan", "ABC", False)
        customer2 = Customer("Eric", "DEF", True)
        myStore = Store()
        myStore.add_member(customer1)
        myStore.add_member(customer2)
        myStore.add_product(checkers)
        myStore.add_product(chess)

        # adding a product to member cart
        product_added = myStore.add_product_to_member_cart(926, "ABC")
        self.assertEqual(product_added, "product added to cart")
        self.assertNotEqual(product_added, "product out of stock")
        checkout_abc = myStore.check_out_member("ABC")
        self.assertNotEqual(checkout_abc, 50) # Price will not be $50 but 50 * .07 since ABC is not a premium member
        checkers_availability = checkers.get_quantity_available()
        self.assertEqual(checkers_availability, 4) # will be 4 since 5 - 1 is equal to 4

        try:
            myStore.check_out_member("XYZ")
        except InvalidCheckoutError:
            print("ID does not match any known member")

        checkout = myStore.check_out_member("DEF")
        self.assertEqual(checkout, 0)
        myStore.add_product_to_member_cart(641, "DEF")
        myStore.add_product_to_member_cart(641, "DEF")  # Since availability is 0, product will not be deducted
        new_checkout = myStore.check_out_member("DEF")
        self.assertNotEqual(new_checkout, 0)
        chess_availability = chess.get_quantity_available()
        self.assertEqual(chess_availability, 0)
        self.assertEqual(new_checkout, 25) # $25 dollars will be total since DEF is a premium member


if __name__ == "__main__":
    unittest.main()
