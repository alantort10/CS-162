# Author: Alan Tort
# Date: 6/22/2021
# Description: Assignment #2, An Online Store Simulator

class InvalidCheckoutError(Exception):
    """To be raised in a try-catch block"""
    pass


class Product:
    """Product object represents a product with an ID code, title, description, price and quantity available"""

    def __init__(self, product_id, title, description, price, quantity_available):
        """Init method"""
        self._product_id = product_id
        self._title = title
        self._description = description
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        """Gets Product's ID"""
        return self._product_id

    def get_title(self):
        """Gets Product's title"""
        return self._title

    def get_description(self):
        """Gets Product's description"""
        return self._description

    def get_price(self):
        """Gets Product's price"""
        return self._price

    def get_quantity_available(self):
        """Gets Product's available quantity"""
        return self._quantity_available

    def decrease_quantity(self):
        """Decreases the available quantity by 1"""
        self._quantity_available -= 1


class Customer:
    """Customer object represents a customer with a name and account ID. Customers must be members of the Store to make
    a purchase. Premium members get free shipping."""

    def __init__(self, name, customer_id, premium_member):
        """Init method"""
        self._name = name
        self._customer_id = customer_id
        self._premium_member = premium_member
        self._cart = list()

    def get_name(self):
        """Gets Customer's name"""
        return self._name

    def get_customer_id(self):
        """Gets Customer's ID"""
        return self._customer_id

    def is_premium_member(self):
        """Returns whether the customer is a premium member (True or False)"""
        return self._premium_member

    def add_product_to_cart(self, product_id):
        """Takes a product ID code and adds it to the Customer's cart"""
        self._cart.append(product_id)

    def get_cart(self):
        """Gets the Customer's cart"""
        return self._cart

    def empty_cart(self):
        """Empties the Customer's cart"""
        self._cart.clear()


class Store:
    """Store object represents a store, which has some number of products in its inventory and some number of customers
    as members"""

    def __init__(self):
        """Init method"""
        self._inventory = dict()
        self._membership = dict()

    def add_product(self, product):
        """Takes a Product and adds it to the inventory dictionary"""
        self._inventory[product.get_product_id()] = product
        return "product added to Store inventory"

    def add_member(self, customer):
        """Takes a Customer and adds it to the membership"""
        self._membership[customer.get_customer_id()] = customer
        return "member added to Store membership"

    def lookup_product_from_id(self, product_id):
        """Takes a Product ID and returns the Product with the matching ID. If no matching ID is found in the inventory,
        it returns the special value None"""
        if product_id in self._inventory:
            return self._inventory[product_id]
        else:
            return None

    def lookup_member_from_id(self, customer_id):
        """Takes a Customer ID and returns the Customer with the matching ID. If no matching gID is found in the
        membership, it returns the special value None"""
        if customer_id in self._membership:
            return self._membership[customer_id]
        else:
            return None

    def product_search(self, search):
        """Takes a search string and returns a lexicographically sorted list of ID codes for every product in the
        inventory whose title or description contains the search string. The search should be case-insensitive. The
        list of codes should not contain duplicates. If the search string is not found, returns an empty list"""
        id_codes = list()
        for item in self._inventory:
            title = self._inventory[item].get_title()
            description = self._inventory[item].get_description()
            if search.lower() in title.lower() or search.lower() in description.lower():
                id_codes.append(item)
        return sorted(id_codes)

    def add_product_to_member_cart(self, product_id, customer_id):
        """Takes a Product ID and a Customer ID and adds the Product corresponding to the Product ID to the Customer's
        cart. There must be at least one of each product added to be added to the customer's cart"""

        if product_id not in self._inventory:
            return "product id not found"

        if customer_id not in self._membership:
            return "member id not found"

        if self._inventory[product_id].get_quantity_available() > 0:
            self._membership[customer_id].add_product_to_cart(product_id)
            return "product added to cart"
        else:
            return "product out of stock"

    def check_out_member(self, customer_id):
        """Takes a customer id, raises an exception if the id does not match a member of the Store, otherwise it returns
        the charge for the member's cart. Non-members pay a 7% percent shipping cost charge of the cart subtotal"""
        if customer_id not in self._membership:
            raise InvalidCheckoutError

        charge = 0
        member = self._membership[customer_id]

        for item in member.get_cart():
            product = self._inventory[item]
            if product.get_quantity_available() > 0:
                charge += product.get_price()
                product.decrease_quantity()

        if member.is_premium_member() is False:
            charge += (charge * 0.07)

        member.empty_cart()
        return charge


def main():
    p1 = Product("BCA", "Xbox Series X", "console", 500, 2)  # Creates a product
    print("Product 1", "\nid:", p1.get_product_id(), "\ntitle:", p1.get_title(), "\ndescription:", p1.get_description(),
          "\nquantity available:", p1.get_quantity_available())
    p2 = Product("ABC", "Xbox Series-S", "console", 300, 5)  # Creates a 2nd product
    print("\nProduct 2", "\nid:", p2.get_product_id(), "\ntitle:", p2.get_title(), "\ndescription:",
          p2.get_description(),
          "\nquantity available:", p2.get_quantity_available())
    p3 = Product("XYZ", "Sony Playstation 5", "console", 500, 0)  # Creates a 3rd product
    print("\nProduct3:", "\nid:", p3.get_product_id(), "\ntitle:", p3.get_title(), "\ndescription:",
          p3.get_description(),
          "\nquantity available:", p3.get_quantity_available())

    myStore = Store()  # creates a store
    print("\nadding Product 1 to Store inventory:", myStore.add_product(p1))
    print("adding Product 2 to Store inventory:", myStore.add_product(p2))
    print("adding Product 3 to Store inventory:", myStore.add_product(p3))

    print("\nSearch results for 'console': ", myStore.product_search("console"))
    print("Search results for 'xbox': ", myStore.product_search("xbox"))
    print("Search results for 'series': ", myStore.product_search("series"))
    print("Search results for 'sony': ", myStore.product_search("sony"))

    c1 = Customer("Alan", "AMT", False)  # Creates a non-premium member customer
    print("\nCustomer1:", "\nname:", c1.get_name(), "\nid:", c1.get_customer_id(), "\npremium_member:",
          c1.is_premium_member())

    print("\nAdd Customer1 to Store membership:", myStore.add_member(c1))

    print("\n1 Xbox Series-X selected")
    print(myStore.add_product_to_member_cart("BCA", "AMT"))  # Adds product 1 to member's cart
    print("\n1 Xbox Series-S selected")
    print(myStore.add_product_to_member_cart("ABC", "AMT"))  # Adds product 2 to member's cart
    print("\n1 Sony Playstation 5 selected")
    print(myStore.add_product_to_member_cart("XYZ", "AMT"))  # Adds product 3 to member's cart

    print("\nTotal amount due for Alan: $", myStore.check_out_member("AMT"))  # Checks out the member, returns cart
    # totals

    print(p1.get_title(), "availability:", p1.get_quantity_available())
    print(p2.get_title(), "availability:", p2.get_quantity_available())
    print(p3.get_title(), "availability:", p3.get_quantity_available())

    c2 = Customer("Eric", "EFT", True)  # Creates a premium member customer
    print("\nCustomer2:", "\nname:", c2.get_name(), "\nid:", c2.get_customer_id(), "\npremium_member:",
          c2.is_premium_member())

    print("\nAdd Customer2 to Store membership:", myStore.add_member(c2))  # add customer to the store

    print("\n1 Xbox Series-X selected")
    print(myStore.add_product_to_member_cart("BCA", "EFT"))  # Adds product 1 to member's cart
    print("\n1 Xbox Series-X selected")
    print(myStore.add_product_to_member_cart("BCA", "EFT"))  # Since stock is already 0, item will not be added to cart
    print("\nTry checking out 'NOT_EFT'")
    try:
        myStore.check_out_member("NOT_EFT")  # Code to raise exception
    except InvalidCheckoutError:
        print("ID does not match any known member")  # Exception is thrown, then program continues...

    print("\nTotal amount due for", c2.get_name(), "$", myStore.check_out_member("EFT"))

    print(p1.get_title(), "availability:", p1.get_quantity_available())
    print(p2.get_title(), "availability:", p2.get_quantity_available())
    print(p3.get_title(), "availability:", p3.get_quantity_available())


if __name__ == "__main__":
    main()
