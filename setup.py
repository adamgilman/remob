from distutils.core import setup
setup(
  name = 'remob',
  packages = ['remob'], # this must be the same as the name above
  version = '0.1',
  description = 'REMote OrderBook is a Python based, redis backed, order book for financial instruments which allows an order book to be kept remotely on redis and accessed for analysis quickly and easily.',
  author = 'Adam Gilman',
  author_email = 'adam.gilman@gmail.com',
  url = 'https://github.com/adamgilman/remob', # use the URL to the github repo
  download_url = 'https://github.com/adamgilman/remob/archive/0.1.zip', # I'll explain this in a second
  keywords = [], # arbitrary keywords
  classifiers = [],
)