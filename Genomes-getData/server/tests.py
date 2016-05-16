import unittest
import models
import controller
import server

class userCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    def test_equal_numbers(self):
        self.assertEqual(2, 2)

    def test_equal_numbers(self):
        self.assertEqual(2, 2)

    @classmethod
    def tearDownClass(cls):
        models.db_session.remove()


if __name__ == '__main__':
    unittest.main()
