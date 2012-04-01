import os

HOST = '0.0.0.0'
PORT = '8030'
STATIC_URL = 'http://somewebsite.com/downloads/''
STATIC_LOCAL = '/some/local/downloads/folder/'
STATIC_LOCAL = os.path.abspath(STATIC_LOCAL)

subdir = "/index/"  #web_route needs to be surrounded by 2 / /
DATE_FORMAT = "%d-%b-%y" #30-Mar-2012
