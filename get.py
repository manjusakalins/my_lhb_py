# -*- coding: utf-8 -*-
import urllib2
import urllib  
import simplejson as json  
import time
import os
import socket
import random
import threading
import sh
import sz
import common_api
import gen_excel
import datetime
import lhb_keeper
import lhb_socket


sd=datetime.date(2013,9,10);
d=datetime.date(2015,9,4);
lhb_socket.lhb_sock_process_period(sd, d)
#gen_excel.excel_do_gen()



