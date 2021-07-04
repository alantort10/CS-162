# Author: Alan Tort
# Date: 6/29/2021
# Description: Project 3: Library Simulator

class LibraryItem:
    """Represents a library item in the library with characteristics
    to be shared amongst the books, albums, and movies"""

    def __init__(self, library_item_id, title):
        """Init method"""
        self._library_item_id = library_item_id  # unique identifier for a LibraryItem
        self._title = title  # cannot be assumed to be unique
        self._location = "ON_SHELF"  # LibraryItem location is either ON_SHELF or ON_HOLD_SHELF or CHECKED_OUT
        self._checked_out_by = None  # refers to the Patron who has it checked out (if any)
        self._requested_by = None  # refers to the Patron who has requested it (if any)
        # a LibraryItem can only be requested by one Patron at a time
        self._date_checked_out = None  # to be set to the current_date of the Library

    def get_library_item_id(self):
        """Gets the library item's id"""
        return self._library_item_id

    def get_title(self):
        """Gets the library item's title"""
        return self._title

    def get_location(self):
        """Gets the LibraryItem's location"""
        return self._location

    def set_location(self, location):
        """Sets the LibraryItem's location to the given location"""
        self._location = location

    def get_checked_out_by(self):
        """Gets the Patron who has checked out the LibraryItem or None"""
        return self._checked_out_by

    def set_checked_out_by(self, patron):
        """Sets who the LibraryItem was checked out by to the given patron"""
        self._checked_out_by = patron

    def get_requested_by(self):
        """Gets the patron who has requested the LibraryItem or None"""
        return self._requested_by

    def set_requested_by(self, patron):
        """Sets who the LibraryItem was requested by to the given patron"""
        self._requested_by = patron

    def get_date_checked_out(self):
        """Gets the date the LibraryItem was checked out"""
        return self._date_checked_out

    def set_date_checked_out(self, date):
        """Sets which day the LibraryItem was checked out"""
        self._date_checked_out = date


class Book(LibraryItem):
    """Represents a book LibraryItem that contains an author attribute and a check out length of 21 days"""

    def __init__(self, library_item_id, title, author):
        """Init method"""
        super().__init__(library_item_id, title)
        self._author = author
        self._check_out_length = 21

    def get_author(self):
        """Gets the author of Book"""
        return self._author

    def get_check_out_length(self):
        """Gets the check out length"""
        return self._check_out_length


class Album(LibraryItem):
    """Represents an album LibraryItem that contains an artist attribute and a check out length of 14 days"""

    def __init__(self, library_item_id, title, artist):
        """Init method"""
        super().__init__(library_item_id, title)
        self._artist = artist
        self._check_out_length = 14

    def get_artist(self):
        """Gets the artist of the Album"""
        return self._artist

    def get_check_out_length(self):
        """Gets the check out length"""
        return self._check_out_length


class Movie(LibraryItem):
    """Represents a movie LibraryItem that contains a director attribute and a check out length of 7 days"""

    def __init__(self, library_item_id, title, director):
        """Init method"""
        super().__init__(library_item_id, title)
        self._director = director
        self._check_out_length = 7

    def get_director(self):
        """Gets the director of the Movie"""
        return self._director

    def get_check_out_length(self):
        """Gets the check out length"""
        return self._check_out_length


class Patron:
    """Represents a library patron with a unique ID, name, list of items checked out
    and late fine amount."""

    def __init__(self, patron_id, name):
        """Init method"""
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_fine_amount(self):
        """Gets the patron's fine amount."""
        return self._fine_amount

    def add_library_item(self, library_item):
        """Adds the specified LibraryItem to checked out items."""
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """Removes the specified LibraryItem from checked out items."""
        self._checked_out_items.remove(library_item)

    def amend_fine(self, amount):
        """Increases or decreases the current fine amount by a certain amount."""
        # negative amount will decrease it, positive amount will increase
        self._fine_amount += amount

    def get_patron_id(self):
        """Returns the patron ID"""
        return self._patron_id

    def get_checked_out_items(self):
        """Gets the library items the patron has checked out."""
        return self._checked_out_items


class Library:
    """Represents a library with holdings, members, and the current date."""

    def __init__(self):
        """Init method"""
        self._holdings = dict()
        self._members = dict()
        self._current_date = 0

    def add_library_item(self, library_item):
        """Adds the specified library item to the library's holdings."""
        self._holdings[library_item.get_library_item_id()] = library_item

    def add_patron(self, patron):
        """Adds the specified patron to the library's members."""
        self._members[patron.get_patron_id()] = patron

    def get_library_item_from_id(self, library_item_id):
        """Returns the LibraryItem object corresponding to the ID given or none."""
        if library_item_id in self._holdings:
            return self._holdings[library_item_id]
        else:
            return None

    def get_patron_from_id(self, patron_id):
        """Returns the Patron object corresponding to the ID given or none."""
        if patron_id in self._members:
            return self._members[patron_id]
        else:
            return None

    def check_out_library_item(self, patron_id, library_item_id):
        """Attempts to check out the patron with the specified library item."""
        # Case where the patron is not in the library's members
        if patron_id not in self._members:
            return "patron not found"

        # Case where the item is not in the holdings
        if library_item_id not in self._holdings:
            return "item not found"

        library_item = self.get_library_item_from_id(library_item_id)
        patron = self.get_patron_from_id(patron_id)

        # Case where item is already checked out
        if library_item.get_checked_out_by() is not None:
            return "item already checked out"

        # Case where the item is on hold
        if library_item.get_requested_by() is not None and library_item.get_requested_by() != patron:
            return "item on hold by other patron"

        # Successful check out
        library_item.set_checked_out_by(patron)
        library_item.set_date_checked_out(self._current_date)
        library_item.set_location("CHECKED_OUT")

        # Case where the item was requested by this patron
        if library_item.get_requested_by() == patron:
            library_item.set_requested_by(None)

        patron.add_library_item(library_item)
        return "check out successful"

    def return_library_item(self, library_item_id):
        """Takes a library item ID and attempts to return the specified library item."""
        # Case where the item is not in the holdings
        if library_item_id not in self._holdings:
            return "item not found"

        # Case where the library item is not checked out
        library_item = self.get_library_item_from_id(library_item_id)
        if library_item.get_checked_out_by() is None:
            return "item already in library"

        # Successful return
        patron = library_item.get_checked_out_by()
        patron.remove_library_item(library_item)

        # Update location
        # Case where another patron has it requested
        if library_item.get_requested_by() is not None:
            library_item.set_location("ON_HOLD_SHELF")

        # Case where it is not requested
        else:
            library_item.set_location("ON_SHELF")

        library_item.set_checked_out_by(None)
        return "return successful"

    def request_library_item(self, patron_id, library_item_id):
        """Takes a patron ID and library item ID and attempts to return that item."""
        # Case where patron is not a member
        if patron_id not in self._members:
            return "patron not found"

        # Case where the library item is not in the holdings
        if library_item_id not in self._holdings:
            return "item not found"

        # Case where the item is already requested
        library_item = self.get_library_item_from_id(library_item_id)
        patron = self.get_patron_from_id(patron_id)
        if library_item.get_requested_by() is not None:
            return "item already on hold"

        # Successful request
        library_item.set_requested_by(patron)

        # Update the location if it is on the shelf
        if library_item.get_location() == "ON_SHELF":
            library_item.set_location("ON_HOLD_SHELF")

        return "request successful"

    def pay_fine(self, patron_id, amount):
        """Takes a patron ID and dollar amount and attempts to pay their overdue fine."""
        if patron_id not in self._members:
            return "patron not found"

        patron = self.get_patron_from_id(patron_id)
        amount = -amount
        patron.amend_fine(amount)
        return "payment successful"

    def increment_current_date(self):
        """Increments the current date and increases each patron's fines by 10 cents
        for each overdue item they have checked out."""
        self._current_date += 1

        # Check for overdue items
        for patron in self._members.values():
            for library_item in patron.get_checked_out_items():
                if self._current_date - library_item.get_date_checked_out() > library_item.get_check_out_length():
                    patron.amend_fine(0.1)


def main():
    b1 = Book("345", "Phantom Tollbooth", "Juster")
    print("Creating Book:", b1)
    a1 = Album("456", "...And His Orchestra", "The Fastbacks")
    print("Creating Album:", a1)
    m1 = Movie("567", "Laputa", "Miyazaki")
    print("Creating Movie:", m1)
    print("Getting Book's author:", b1.get_author())
    print("Getting Album's artist:", a1.get_artist())
    print("Getting Movie's director:", m1.get_director())

    p1 = Patron("abc", "Felicity")
    p2 = Patron("bcd", "Waldo")

    lib = Library()
    print("Creating Library", lib)
    lib.add_library_item(b1)
    print("Adding Book")
    lib.add_library_item(a1)
    print("Adding Album")
    lib.add_patron(p1)
    print("Adding Patron 1")
    lib.add_patron(p2)
    print("Adding Patron 2")

    print("Patron 2 checking out Album:", lib.check_out_library_item("bcd", "456"))
    print("Patron 2's checked out items:", p2.get_checked_out_items())
    loc = a1.get_location()
    print("item location:", loc)
    print("Patron 1 requesting same Album:", lib.request_library_item("abc", "456"))
    print("Patron 1 checking out same Album:", lib.check_out_library_item("abc", "456"))
    for i in range(57):
        lib.increment_current_date()  # 57 days pass
    print("57 days pass")
    p2_fine = p2.get_fine_amount()
    p1_fine = p1.get_fine_amount()
    print("Patron 2's fine:", p2_fine)
    print("Patron 1's fine:", p1_fine)
    print("Patron 2 paying fine:", lib.pay_fine("bcd", p2_fine))
    print("Patron 2 returning item:", lib.return_library_item("456"))


if __name__ == "__main__":
    main()
