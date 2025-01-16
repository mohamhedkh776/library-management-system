import unittest
from library_management_system import LibraryManagementSystem

class TestLibraryManagementSystem(unittest.TestCase):
    def setUp(self):
        self.library = LibraryManagementSystem()

    def test_add_book(self):
        self.library.add_book("Title1", "Author1", "123")
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]["title"], "Title1")
        
        with self.assertRaises(ValueError):
            self.library.add_book("", "Author2", "124")
        
        with self.assertRaises(ValueError):
            self.library.add_book("Title1", "Author1", "123")

    def test_borrow_book(self):
        self.library.add_book("Title2", "Author2", "456")
        result = self.library.borrow_book("456")
        self.assertEqual(result, "Book 'Title2' borrowed successfully.")
        
        result = self.library.borrow_book("456")
        self.assertEqual(result, "Book 'Title2' is not available.")
        
        result = self.library.borrow_book("999")
        self.assertEqual(result, "Book not found.")

    def test_return_book(self):
        self.library.add_book("Title3", "Author3", "789")
        self.library.borrow_book("789")
        
        result = self.library.return_book("789")
        self.assertEqual(result, "Book 'Title3' returned successfully.")
        
        result = self.library.return_book("789")
        self.assertEqual(result, "Book 'Title3' is already available.")
        
        result = self.library.return_book("999")
        self.assertEqual(result, "Book not found.")

    def test_search_book(self):
        self.library.add_book("Python Programming", "John Doe", "101")
        self.library.add_book("Learn Python", "Jane Smith", "102")

        results = self.library.search_book(title="Python")
        self.assertEqual(len(results), 2)

        results = self.library.search_book(author="Jane")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["isbn"], "102")

        results = self.library.search_book(isbn="101")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Python Programming")

        # Cover case where no parameters are passed to search_book
        results = self.library.search_book()
        self.assertEqual(len(results), 2)

        # Cover case where no books exist in the library
        empty_library = LibraryManagementSystem()
        results = empty_library.search_book()
        self.assertEqual(len(results), 0)

    def test_list_available_books(self):
        # Test with no books in the library
        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 0)

        # Test with all books available
        self.library.add_book("Title4", "Author4", "111")
        self.library.add_book("Title5", "Author5", "112")
        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 2)

        # Test when some books are borrowed
        self.library.borrow_book("111")
        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 1)
        self.assertEqual(available_books[0]["isbn"], "112")

    def test_list_available_books_edge_case(self):
        # Test when all books are borrowed
        self.library.add_book("Title6", "Author6", "113")
        self.library.add_book("Title7", "Author7", "114")
        self.library.borrow_book("113")
        self.library.borrow_book("114")

        available_books = self.library.list_available_books()
        self.assertEqual(len(available_books), 0)  # No books should be available

if __name__ == "__main__":
    unittest.main()
