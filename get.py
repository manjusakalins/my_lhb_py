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

sd=datetime.date(2015,12,4);
d=datetime.date(2015,12,8);
lhb_keeper.lhb_process_period(sd, d)
gen_excel.excel_do_gen()


