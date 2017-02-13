from collections import namedtuple

Order = namedtuple("Order", ['order_id', 'time', 'price', 'quantity'])
Match = namedtuple("Match", ['bid_id', 'ask_id', 'price', 'quantity'])