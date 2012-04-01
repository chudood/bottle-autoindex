import os

HOST = '0.0.0.0'
PORT = '8030'
STATIC_URL = 'http://www.metachu.com:9092/downloads/'
STATIC_LOCAL = '/home/chu/'
STATIC_LOCAL = os.path.abspath(STATIC_LOCAL)

subdir = "/"
DATE_FORMAT = "%d-%b-%y" #30-Mar-2012
