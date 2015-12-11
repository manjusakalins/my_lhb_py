# -*- coding: utf-8 -*-
import urllib2
import urllib  
import simplejson as json  
import time
import datetime
import os
import socket
import random
import threading
import sh
import sz
import common_api
import gen_excel
import socket
import lhb_sock

class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		#global step3_p_skey
		#print "@@@@@@@@@@@@@ get it @@@@@@@@@@@"
		#step3_p_skey=find_cookie_str(headers.get('Set-Cookie'), "p_skey");
		#print step3_p_skey
		#return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		pass

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(),HttpRedirect_Handler())
d=datetime.date(2015,11,3);
print d.strftime("%d/%m/%y")
print type(d)

def my_url_read_data(url, body_values, headers, stimeout=5):
	print url
	global opener
	out_cookies=""
	the_page=""
	req = urllib2.Request(url, body_values, headers)
	try:
		if stimeout == 0:
			response = opener.open(req)
		else:
			response = opener.open(req,timeout=stimeout)
		the_page = response.read()
		if response.info().has_key('Set-Cookie'):
			out_cookies = response.info()['Set-Cookie']
		#print response.info();
	except:
		print '@@@@@@@@@@@@@@@@@@ error @@@@@@@@@@@@@@@@@@@@@@ at: ' + url; 
	#print "read out: " + the_page
	return [the_page,out_cookies]

def sh_pre_process_lhb_data(data):
	js_data=data.split("({")[1].split("})")[0];
	js_data="{"+js_data+"}"
	ret_js=json.loads(js_data,encoding="utf-8")
	#print ret_js['dateTx'];
	#print ret_js['fileContents']
	file_lines=ret_js['fileContents']
	return file_lines;

###########################shang hai.##########################
def sh_lhb_get_one_date_data(dtime):
	if type(dtime) != datetime.date:
		print "##$$### error datetime input"
		return;
	
	if not common_api.date_is_workday(dtime):
		return "";
	
	file_name="lhb/sh"+dtime.isoformat();
	print "try get "+file_name

	
	#if already exist.
	if os.path.isfile(file_name):
		rf=open(file_name, "r")
		data=rf.read();
		if len(data) > 100:
			return sh_pre_process_lhb_data(data);
	

	#not exist
	user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
	refstr='http://www.sse.com.cn/disclosure/diclosure/public/'
	headers = { 'User-Agent' : user_agent,
				'Referer' : refstr,
				'Connection' : 'keep-alive',
				}
	http_body = None
	url='http://query.sse.com.cn/infodisplay/showTradePublicFile.do?jsonCallBack=jQuery172007153944508172572_1449041339236&dateTx='+dtime.isoformat()+'&random=0.983882803004235&_=1449041354010'
	print url;
	data=my_url_read_data(url, http_body, headers)[0];
	
	wf=open(file_name, "w");
	wf.write(data);
	wf.close();
	return sh_pre_process_lhb_data(data);

###########################shen zhen##########################
def sz_lhb_get_one_date_data(dtime, where):

	if not common_api.date_is_workday(dtime):
		return "";
	file_name="lhb/sz"+where+dtime.isoformat();
	print "try get "+file_name

	#if already exist.
	if os.path.isfile(file_name):
		rf=open(file_name, "r")
		data=rf.read();
		rf.close();
		if len(data) > 100:	
			return data;

	#get from web.
	user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
	if where == "zb":
		refstr='http://www.szse.cn/main/disclosure/news/scgkxx/'
		baseurl='http://www.szse.cn/szseWeb/common/szse/files/text/jy/jy'
	if where == "cyb":
		refstr='http://www.szse.cn/main/chinext/jygkxx/jygkxx/'
		baseurl='http://www.szse.cn/szseWeb/common/szse/files/text/nmTxt/gk/nm_jy'
	if where == "zxb":
		refstr='http://www.szse.cn/main/sme/jytj/jygkxx/'
		baseurl='http://www.szse.cn/szseWeb/common/szse/files/text/smeTxt/gk/sme_jy'
	
	headers = { 'User-Agent' : user_agent,
				'Referer' : refstr,
				'Connection' : 'keep-alive',
				'Content-Type' : 'application/x-www-form-urlencoded; charset=utf-8',
				}
	http_body = None
	url=baseurl+dtime.strftime("%y%m%d")+'.txt?randnum=0.44545467011630535'

	print url;
	data=my_url_read_data(url, http_body, headers)[0];
	data=data.decode('gbk').encode("utf-8");
	#print data;
	wf=open(file_name, "w");
	wf.write(data);
	wf.close();
	return data;


def lhb_sz_process(d):
	data=sz_lhb_get_one_date_data(d,"zxb");
	data=data.split("\n");
	sz.sz_gen_record_from_data(data)
	
	data=sz_lhb_get_one_date_data(d,"cyb");
	data=data.split("\n");
	sz.sz_gen_record_from_data(data)
	
	data=sz_lhb_get_one_date_data(d,"zb");
	data=data.split("\n");
	sz.sz_gen_record_from_data(data)

def lhb_sh_process(d):
	data=sh_lhb_get_one_date_data(d);
	sh.sh_gen_record_from(data)


def lhb_process_one_date(d):
	lhb_sz_process(d)
	lhb_sh_process(d)
	
def lhb_process_period(start_d, end_d):
	while end_d >= start_d:
		lhb_process_one_date(start_d);
		start_d = start_d + datetime.timedelta(days=1);

####===================================================================
def lhb_sock_return_data_onwhere(onwhere,data):
	if 'sh' == onwhere:
		return sh_pre_process_lhb_data(data)
	else:
		return data;

def lhb_sock_process_one_date_where(onwhere,dtime):
	
	if not common_api.date_is_workday(dtime):
		return "";
	file_name="lhb/"+onwhere+where+dtime.isoformat();
	print "try get "+file_name

	#if already exist.
	if os.path.isfile(file_name):
		rf=open(file_name, "r")
		data=rf.read();
		rf.close();
		if len(data) > 100:
			return lhb_sock_return_data_onwhere(onwhere, data);
	#socket read out data:
	lhb_socket.lhb_socket_read_sz(onwhere,dtime)
	#print data;
	wf=open(file_name, "w");
	wf.write(data);
	wf.close();
	return lhb_sock_return_data_onwhere(onwhere, data);
	
	
def lhb_sock_process_period(start_d, end_d):
	while end_d >= start_d:
		lhb_process_one_date(start_d);
		start_d = start_d + datetime.timedelta(days=1);


