import unittest
from remob import SyncOrderBook, OrderBook

class TestBasicObjects(unittest.TestCase):
	def setUp(self):
		self.sob = SyncOrderBook()
		self.ob = OrderBook()

	def test_sync_ob_object(self):
		self.assertEqual(type(self.sob), SyncOrderBook)
		self.assertEqual(type(self.ob), OrderBook)