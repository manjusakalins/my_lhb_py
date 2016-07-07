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
import httplib2

h = httplib2.Http(".cache")

class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		#global step3_p_skey
		#print "@@@@@@@@@@@@@ get it @@@@@@@@@@@"
		#step3_p_skey=find_cookie_str(headers.get('Set-Cookie'), "p_skey");
		#print step3_p_skey
		#return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		pass

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(),HttpRedirect_Handler())
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
	

def sz_lhb_get_one_date_data(dtime, where):

	if not common_api.date_is_workday(dtime):
		return "";
	file_name="lhb/111"+where+dtime.isoformat();
	print "try get "+file_name



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
	resp, content = h.request(url,headers=headers)
	data = content;
	print data
	data=data.decode('gbk').encode("utf-8");
	#print data;
	wf=open(file_name, "w");
	wf.write(data);
	wf.close();
	return data;
	

headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Charset": "UTF-8;q=0.5",
      "Accept-Encoding": "gzip,deflate,sdch",
      "Accept-Language": "zh-CN,zh;q=0.8",
      "Cache-Control": "max-age=0",
      "Connection": "keep-alive",
      "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91   Safari/534.30",
}

resp, content = h.request("http://pan.baidu.com/share/link?shareid=3910200743&uk=2651292192",headers=headers)
#print resp,'\n\n\n\n\n',content
resp, content = h.request("http://soso.com/q?pid=s.idx&cid=s.idx.se&w=ubuntu-12.04*.iso+site%3Apan.baidu.com",headers=headers)
#print resp


d=datetime.date(2015,11,6);
sz_lhb_get_one_date_data(d, "cyb");

