# -*- coding: utf-8 -*-
import urllib2
import urllib  
import simplejson as json  
import time
import os
import socket
import random
import threading

base_money=100000000
'''
code,name,date,reason,buy(who,b,s),sell(who,b,s),
	
'''
g_rec={};
def record_gen_and_init(code,name, date, reason, total_money=0, notion=""):
	record={}
	record['code'] = code;
	record['name'] = name;
	record['date'] = date;
	record['reason'] = reason;
	record['total_money'] = total_money;
	record['notion'] = notion;
	record['buy'] = [];
	record['sell'] = [];
	return record;

def record_add_one_list(record, key, who, buy, sell):
	record[key].append({"who":who, "buy":buy, "sell":sell})
	
def record_join_to_global(record):
	if g_rec.get(record['code']) == None:
		g_rec[record['code']] = [];
	g_rec[record['code']].append(record);


def str_get_str_between(ori,front,back):
	if front != "" and ori.find(front) != -1:
		return ori.split(front)[1].split(back)[0].strip();
	if front == "" and ori.find(back) != -1:
		return ori.split(back)[0].strip();
	return ""
	

def stock_get_notion_ths(code):
	#curl 'http://stockpage.10jqka.com.cn/300104/'
	renotion=""
	cmd_url = 'curl --connect-timeout 2 -m 2 http://stockpage.10jqka.com.cn/' + str(code) + '/'
	web=os.popen(cmd_url).readlines();
	for idx in range(len(web)):
		line=web[idx];
		if line.find("<dt>涉及概念：</dt>") != -1:
			lines=web[idx+1];#+web[idx+2];
			lines=lines.split("\"");
			print lines[1];
			renotion=lines[1];
			break;
	return renotion;

def xlsxwriter_write_chinese(ws,row_idx,col_idx,data, cell_format=None):
	if type(data) == str:
		ws.write(row_idx, col_idx, data.decode("utf-8"),cell_format);
	else:
		ws.write(row_idx, col_idx, data,cell_format);
		
def date_is_workday(dtime):
	weekday=dtime.strftime("%w")
	if int(weekday) == 6 or int(weekday) == 0:
		print "not workday" + str(weekday)
		return 0;
	return 1;
