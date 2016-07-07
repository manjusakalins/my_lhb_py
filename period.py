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

gen_excel.gen_excel_init();
#sd=datetime.date.today();
sd=datetime.date(2014,8,29);
#ed=datetime.date(2013,11,26);
#sd = sd - datetime.timedelta(days=1);
ed=datetime.date.today();
lhb_socket.lhb_sock_process_period(sd, ed)
gen_excel.excel_do_gen()



