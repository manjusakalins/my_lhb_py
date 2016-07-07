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


sd=datetime.date.today();
#d=datetime.date(2015,12,11);
start_d = sd - datetime.timedelta(days=1);
lhb_socket.lhb_sock_process_period(start_d, start_d)
gen_excel.excel_do_gen()



