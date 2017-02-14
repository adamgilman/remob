import sys
sys.path.append( "../" )

import time, redis, GDAX
from remob import SyncOrderBook

r = redis.Redis()
sob = SyncOrderBook("BTCUSD", r)

# Following the process listed here
# https://docs.gdax.com/#real-time-order-book
'''
1) Send a subscribe message for the product of interest.
2) Queue any messages received over the websocket stream.
3) Make a REST request for the order book snapshot from the REST feed.
4) Playback queued messages, discarding sequence numbers before or equal to the snapshot sequence number.
5) Apply playback messages to the snapshot as needed (see below).
6) After playback is complete, apply real-time stream messages as they arrive.
'''
products = 'BTC-USD'

#get current pricing for pairs

gx = GDAX.PublicClient()
p_price = gx.getProductTicker(product=products)
print p_price

#start streaming prices
class updateStream(GDAX.WebsocketClient):
        def open(self):
            print "GDAX Connection Opened - %s\n" % self.product_id
        def message(self, msg):
            #print msg
            print msg
            '''
            if msg['type'] == 'match':
                print msg
                if msg['side'] == 'sell':
                    r.hmset(msg['product_id'], {'ask':msg['price']})
                if msg['side'] == 'buy':
                    r.hmset(msg['product_id'], {'bid':msg['price']})
                #r.hmset(self.product_id, {'bid':p_price['bid'], 'ask':p_price['ask']})
			'''
        def closed(self):
            print "GDAX Connection Closed - %s\n" % self.product_id

ws = updateStream(product_id=products)

