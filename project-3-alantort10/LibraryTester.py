# Author: Alan Tort
# Date: 7/2/2021
# Description: Unit Testing for Library.py

import unittest
from Library import LibraryItem
from Library import Book
from Library import Album
from Library import Movie
from Library import Patron
from Library import Library


class test_library(unittest.TestCase):

    def test_library_item(self):
        """Testing methods of the LibraryItem class"""
        new_library_item = LibraryItem(123, "Title")
        id = new_library_item.get_library_item_id()
        title = new_library_item.get_title()
        self.assertEqual(id, 123) # should be True
        self.assertEqual(title, "Title")  # should be True