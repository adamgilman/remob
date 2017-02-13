import unittest
import redis
from unittest import skip
from mock import patch
from mockredis import mock_redis_client

from remob import SyncOrderBook, Order, Match
from remob.syncorderbook import NoOrderFound, BadOrderTypeException, BadMatchTypeException

class TestSyncOrderBook(unittest.TestCase):
	@patch('redis.Redis', mock_redis_client)
	def setUp(self):
		red = redis.Redis()
		self.sob = SyncOrderBook(redis=red)

	def test_book_name(self):
		#generate a random bookname, so redis gets a unique keyspace
		self.assertTrue(self.sob.bookname is not None)

	def test_add_takes_order_type(self):
		self.assertRaises(BadOrderTypeException, self.sob.bid.add, None)
		self.assertRaises(BadOrderTypeException, self.sob.ask.add, None)

	def test_order_on_book(self):
		new_order_d = {
			'order_id'	: "test_1111",
			'time'		: 1,
			'price'		: 22.22,
			'quantity'	: 10
		}
		new_order = Order(**new_order_d)

		self.sob.bid.add(new_order)
		check_order = self.sob.bid.info(new_order.order_id)
		self.assertEqual(check_order.order_id, new_order.order_id)
		self.assertEqual(check_order.price, new_order.price)

		self.assertRaises(NoOrderFound, self.sob.bid.info, "invalid_order_id")
		

	def test_cancel_on_book(self):
		new_order_d = {
			'order_id'	: "test_1111",
			'time'		: 1,
			'price'		: 22.22,
			'quantity'	: 10
		}
		new_order = Order(**new_order_d)
		self.sob.bid.add(new_order)
		check_order = self.sob.bid.info(new_order.order_id)
		self.assertEqual(check_order.order_id, new_order.order_id)
		self.sob.bid.cancel(new_order.order_id)
		self.assertRaises(NoOrderFound, self.sob.bid.info, new_order.order_id)

	def test_match_takes_match_type(self):
		self.assertRaises(BadMatchTypeException, self.sob.match, None)

	def test_match_on_book_ask_greater(self):
		ask_order = {
			'order_id'	: 'ask_111',
			'time'		: 1,
			'price'		: 10,
			'quantity'	: 100
		}
		self.sob.ask.add( Order(**ask_order) )

		bid_order = {
			'order_id'	: 'bid_111',
			'time'		: 1,
			'price'		: 10,
			'quantity'	: 50	
		}
		self.sob.bid.add( Order(**bid_order) )		

		match_order_d = {
			'bid_id'	: bid_order['order_id'],
			'ask_id'	: ask_order['order_id'],
			'price'		: 10,
			'quantity'	: 50
		}
		match_order = Match(**match_order_d)
		self.sob.match(match_order)

		check_order = self.sob.ask.info(ask_order['order_id'])
		self.assertEqual(check_order.quantity, 50)

		self.assertRaises(NoOrderFound, self.sob.bid.info, bid_order['order_id'])		
	
	def test_match_on_book_bid_full_bid(self):
		ask_order = {
			'order_id'	: 'ask_111',
			'time'		: 1,
			'price'		: 10,
			'quantity'	: 50
		}
		self.sob.ask.add( Order(**ask_order) )

		bid_order = {
			'order_id'	: 'bid_111',
			'time'		: 1,
			'price'		: 10,
			'quantity'	: 50	
		}
		self.sob.bid.add( Order(**bid_order) )

		match_order_d = {
			'bid_id'	: bid_order['order_id'],
			'ask_id'	: ask_order['order_id'],
			'price'		: 10,
			'quantity'	: 50
		}
		match_order = Match(**match_order_d)
		self.sob.match(match_order)

		self.assertRaises(NoOrderFound, self.sob.bid.info, bid_order['order_id'])
		self.assertRaises(NoOrderFound, self.sob.ask.info, ask_order['order_id'])		


	def test_change_order_quantity(self):
		ask_order = {
			'order_id'	: 'ask_111',
			'time'		: 1,
			'price'		: 10,
			'quantity'	: 100
		}
		self.sob.ask.add( Order(**ask_order) )
		self.sob.ask.change(order_id=ask_order['order_id'], quantity=50)
		check_order = self.sob.ask.info(ask_order['order_id'])
		self.assertEqual(check_order.quantity, 50)

	def test_change_order_price(self):
		ask_order = {
			'order_id'	: 'ask_111',
			'time'		: 1,
			'price'		: 10,
			'quantity'	: 100
		}
		self.sob.ask.add( Order(**ask_order) )
		self.sob.ask.change(order_id=ask_order['order_id'], price=50)
		check_order = self.sob.ask.info(ask_order['order_id'])
		self.assertEqual(check_order.price, 50)







