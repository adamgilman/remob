from uuid import uuid4 as uuid
from collections import OrderedDict
import ast

from order import Order, Match

class BadOrderTypeException(Exception): pass
class NoOrderFound(Exception): pass
class BadMatchTypeException(Exception): pass

class SyncOrderBookSide(object):
	def __init__(self, bookname, side, redis):
		self.redis = redis
		self.bookname = bookname
		self.side = side
		self.key = "%(bookname)s:%(side)s" % {'bookname': self.bookname, 'side':self.side}
		self.key_store = "%(bookname)s:%(order_id)s"

	def add(self, new_order):
		if type(new_order) is not Order:
			raise BadOrderTypeException("Must pass Order type as new order to OrderBook")
		hkey = self.key_store % {'bookname':self.bookname, 'order_id':new_order.order_id}
		self.redis.hset(hkey, 'order', dict(new_order._asdict()) )
		self.redis.hset(hkey, 'price', new_order.price)
		self.redis.hset(hkey, 'quantity', new_order.quantity)
		self.redis.hset(hkey, 'time', new_order.time)
		self.redis.zadd(self.key, hkey, new_order.price)

	def cancel(self, order_id):
		self.redis.zrem(self.key, order_id)
		hkey = self.key_store % {'bookname':self.bookname, 'order_id':order_id}
		self.redis.delete(hkey)

	def change(self, order_id, quantity=None, price=None):
		hkey = self.key_store % {'bookname':self.bookname, 'order_id':order_id}
		order = dict( self.info(order_id)._asdict() )
		self.cancel(order_id)
		if quantity is not None:
			order['quantity'] = quantity
		if price is not None:
			order['price'] = price
		order = Order(**order)
		self.add(order)

	def info(self, order_id):
		hkey = self.key_store % {'bookname':self.bookname, 'order_id':order_id}
		r_order = self.redis.hget(hkey, 'order')
		if r_order is not None:
			order = ast.literal_eval( r_order )
			return Order(**order)
		else:
			raise NoOrderFound("No order with that %s found in %s" % (order_id, self.side))

class SyncOrderBook(object):
	def __init__(self, bookname=None, redis=None):
		self.redis = redis
		if bookname is None:
			self.bookname = uuid().hex
		else:
			'''
			if a user passes their ownn bookname
			it is THEIR responsibilty to guarantee
			uniqueness, use at own peril 
			'''
			pass

		self.bid = SyncOrderBookSide(self.bookname, 'bid', self.redis)
		self.ask = SyncOrderBookSide(self.bookname, 'ask', self.redis)

	def match(self, match_order):
		if type(match_order) is not Match:
			raise BadMatchTypeException("Must pass Match type as matching order")

		bid_order = self.bid.info(match_order.bid_id)
		ask_order = self.ask.info(match_order.ask_id)

		new_quantity =  ask_order.quantity - bid_order.quantity
		if new_quantity != 0:
			self.ask.change(order_id=ask_order.order_id, quantity=new_quantity)
		else:
			self.ask.cancel(ask_order.order_id)


		self.bid.cancel(bid_order.order_id)






