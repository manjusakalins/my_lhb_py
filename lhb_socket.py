# -*- coding: utf-8 -*-
import datetime
import socket
import sys
import time

#####################socket start##########################
sz_sock=None;
sh_sock=None;
def lhb_socket_get_create_socket(server):
	#创建套接字
	sock=None;
	try :
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.eorror,e:
		print 'socket false:%s'%e
	print 'socket ...' + str(server)

	#连接百度ip
	try :
		sock.connect((server,80))
	except socket.error,e:
		print 'connect false %s'%e
		sock.close()
		sock=None
	print 'connect ...' + str(server)

	return sock;

def lhb_socket_get_sz_socket():
	global sz_sock;
	if sz_sock!=None:
		return sz_sock;
	sz_sock=lhb_socket_get_create_socket("www.szse.cn");
	return sz_sock;

def lhb_socket_get_sh_socket():
	global sh_sock;
	if sh_sock!=None:
		return sh_sock;
	sh_sock=lhb_socket_get_create_socket("query.sse.com.cn");
	return sh_sock;

def lhb_socket_socket_error(sock):
	global sz_sock;
	global sh_sock;
	if sock==sz_sock:
		sock.close();
		sz_sock=None;
	if sock==sh_sock:
		sock.close();
		sh_sock=None;

def lhb_get_socket_form_where(where):
	if 'sh' == where:
		return lhb_socket_get_sh_socket();
	else:
		return lhb_socket_get_sz_socket();
#####################socket end##########################


############### http get  start ####################################
def lhb_socket_read_httpget(sock,getstr):
	try :
		sock.send(getstr);
	except socket.eorror,e:
		print 'send false'
		lhb_socket_socket_error(sock);

	data=''
	data = sock.recv(1024)
	first=len(data);
	print "first data================start:\n"+data+"\n================end"

	#find content length;
	beg = data.find('Content-Length:',0,len(data))
	end = data.find('\n',beg,len(data))
	if(beg == end):
		print 'connecting closed'
		lhb_socket_socket_error(sock);
		return "";

	print "Content-Length read data:"+data[beg+16:end];
	num = long(data[beg+16:end])

	#find header length;
	beg = data.find('\r\n\r\n',end,len(data))
#	end = data.find('\r\n',beg,len(data))
	head_len=beg+4;
	print "header len:" + str(head_len)
	print data[head_len];
	print data[head_len+1];
	print data[head_len+2];

	#read all data;
	all_data=data;
	while (1):
		data=sock.recv(1024)
		all_data=all_data+data;
		if(len(all_data) >= num+head_len):
			break
	print "all_data len:" + str(len(all_data))
	return all_data[head_len:];


def lhb_gen_str_from_onwhere(where, dtime):
	if where == "zb":
		refstr='http://www.szse.cn/main/disclosure/news/scgkxx/'
		baseurl='/szseWeb/common/szse/files/text/jy/jy'
	if where == "cyb":
		refstr='http://www.szse.cn/main/chinext/jygkxx/jygkxx/'
		baseurl='/szseWeb/common/szse/files/text/nmTxt/gk/nm_jy'
	if where == "zxb":
		refstr='http://www.szse.cn/main/sme/jytj/jygkxx/'
		baseurl='/szseWeb/common/szse/files/text/smeTxt/gk/sme_jy'

	if where == 'sh':
		refstr='http://www.sse.com.cn/disclosure/diclosure/public/'
		geturl='GET /infodisplay/showTradePublicFile.do?jsonCallBack=jQuery17203112255702726543_1449802401736&dateTx='+dtime.isoformat()+'&random=0.6180421001052648&_=1449802771694 HTTP/1.1'
		hoststr='query.sse.com.cn'
	else:
		geturl='''GET '''+baseurl+dtime.strftime("%y%m%d")+'''.txt?randnum=0.4188389303162694 HTTP/1.1'''
		hoststr='www.szse.cn'
		
	return [geturl, hoststr, refstr];


def lhb_check_data_format_form_where(where,all_data):
	try:
		if 'sh' == where:
			#print all_data#.decode("utf-8")
			dd=all_data.decode("utf-8")	
		else:
			dd=all_data.decode("gbk")
		print "check data ok!"
	except:
		print "data error!!!! " + where
		return '';
	#ok and return utf-8
	if 'sh' == where:
		return all_data.encode("utf-8");
	else:
		return all_data.decode("gbk").encode("utf-8");



def lhb_socket_read_onedate_form_where(dtime, where):
	sock=lhb_get_socket_form_where(where);
	strs=lhb_gen_str_from_onwhere(where,dtime);

	print 'send start...'
	#make request str
	getstr=strs[0]+'''
Host: '''+strs[1]+'''
Referer: '''+strs[2]+'''
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Accept: */*
Accept-Language: en-US,en;q=0.8


'''
	print getstr
	
	all_data=lhb_socket_read_httpget(sock,getstr);
	return lhb_check_data_format_form_where(where,all_data) == 0:

############### http get  end ####################################

sd=datetime.date(2015,12,8);
lhb_socket_read_onedate_form_where(sd, 'sh');
lhb_socket_read_onedate_form_where(sd, 'zb');
lhb_socket_read_onedate_form_where(sd, 'cyb');
lhb_socket_read_onedate_form_where(sd, 'zxb');
#lhb_socket_read_sh(sd);
