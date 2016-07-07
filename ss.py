# -*- coding: utf-8 -*-
'''
socket 给百度发送http请求

连接成功后，发送http的get请求，所搜索功能

'''
import socket
import sys
import time
if __name__=='__main__':
	ddd='''HTTP/1.1 200 OK
Cache-Control: max-age=31536000
Content-Length: 15664
Content-Type: text/html;charset=gbk
Last-Modified: Wed, 09 Dec 2015 08:33:40 GMT
Accept-Ranges: bytes
ETag: "c4ec8a4e5c32d11:0"
Server: Microsoft-IIS/6.0
X-Powered-By: ASP.NET
Date: Thu, 10 Dec 2015 09:45:47 GMT
'''
	print len(ddd)
	#创建套接字
	try :
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.eorror,e:
		print 'socket false:%s'%e
	print 'socket ...'

	#连接百度ip
	try :
		sock.connect(('www.szse.cn',80))
	except socket.error,e:
		print 'connect false %s'%e
		sock.close()
	print 'connect ...'

	#发送百度首页面请求并且保持连接
	try :
		print 'send start...'
		#str='GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection:keep-alive\r\n\r\n'
		str='''GET /szseWeb/common/szse/files/text/jy/jy151209.txt?randnum=0.4188389303162694 HTTP/1.1
Host: www.szse.cn
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Accept: */*
Referer: http://www.szse.cn/main/disclosure/news/scgkxx/
Accept-Language: en-US,en;q=0.8


'''
		print str;
		sock.send(str)
	except socket.eorror,e:
		print 'send false'
		sock.close()

	data=''
	data = sock.recv(2024)
	first=len(data);
	while (1):
		'''如何判断数据接收完毕，在发送http 最前端,包含发送数据文件大小属性Content-Length，用字符匹配方式取得文件大小,同过大小判断是否接收完毕。'''
		print "111"+data
		print len(data)
		
		beg = data.find('Content-Length:',0,len(data))
		end = data.find('\n',beg,len(data))
		print beg
		print end
		if(beg == end):
			print 'connecting closed'
			break
		print "read data:"+data[beg+16:end];
		num = long(data[beg+16:end])
		print num
		
		beg = data.find('Date:',0,len(data))
		end = data.find('\r\n',beg,len(data))
		print beg
		print end;
		print "==============="		
		print data[289]
		print data[292]
		print data[293]
		print data[294]
		print data[295]
		print data[296]
		print "==============="
		nums = 0
		tdata=data;
		while (1):
			data=sock.recv(1024)
			tdata=tdata+data;
			#print data#.decode('gbk')
			nums +=len(data)
			if(nums >= num):
				break
			print nums+first;
			if nums+first == 15958:
				print ":dd"
				print tdata[294:].decode('gbk');
				print len(tdata);
				print tdata[0:294]
		word = raw_input('please input your word----->')
		str='''GET /s?wd=''' + word + ''' HTTP/1.1
Host:www.baidu.com
Connection: Keep-Alive

'''
		print str
		sock.send(str)
		data = ''
		data = sock.recv(1024)
	sock.close()
	print data

