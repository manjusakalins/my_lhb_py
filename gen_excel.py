# -*- coding: utf-8 -*-
import urllib2
import urllib
import simplejson as json
import time
import os
import socket
import random
import threading
import common_api

import os
import pickle
import codecs
import sys
import xlrd
from openpyxl import load_workbook
import xlsxwriter
import re
import operator
import random


heads=[u"代码",u"名字", u"日期", u"营业部", u"买入", u"占比", u"卖出", u"占比", u"净值", u"概念", u"备注"]
keys=["code", "name", "date"]#"who", "buy", "sell", ""];
f=open("target_list", 'r');
target_list=f.readlines();
#print lines[0].split()[1];
def excel_check_if_is_target(who):
	for cur_target in target_list:
		if len(cur_target) < 3:
			continue;
		if who.find(cur_target.split()[0]) != -1:
			return [1,cur_target.split()[1]];
	return [0,""];


def excel_gen_all_list_in_record(wb,ws,cur_rec, bskey, row_idx):
	date_format = wb.add_format({'num_format': 'yyyy-m-d','align': 'center'})
	red_format = wb.add_format();red_format.set_font_color('red');
	green_format = wb.add_format();green_format.set_font_color('green');
	for bidx in range(len(cur_rec[bskey])):
		'''
		for col_idx in range(len(keys)):
		print keys[col_idx]
		if type(cur_rec[keys[col_idx]]) == str:
		ws.write(row_idx, col_idx, cur_rec[keys[col_idx]].decode("utf-8"));
		else:
		ws.write(row_idx, col_idx, cur_rec[keys[col_idx]]);
		'''
		re_target=excel_check_if_is_target(cur_rec[bskey][bidx]["who"]);
		if re_target[0] != 1:
			continue;
		col_idx=0;ws.write(row_idx, col_idx, cur_rec["code"]);
		col_idx=col_idx+1;
		if type(cur_rec[keys[col_idx]]) == str:
			ws.write(row_idx, col_idx, cur_rec["name"].decode("utf-8"));
		else:
			ws.write(row_idx, col_idx, cur_rec["name"]);

		#print type(cur_rec["date"])
		col_idx=col_idx+1;ws.write_datetime(row_idx, col_idx, cur_rec["date"], date_format);
		col_idx=col_idx+1;ws.write(row_idx, col_idx, cur_rec[bskey][bidx]["who"].decode("utf-8"));
		col_idx=col_idx+1;ws.write(row_idx, col_idx, cur_rec[bskey][bidx]["buy"], red_format);
		col_idx=col_idx+1;ws.write(row_idx, col_idx, float("%.02f"%(cur_rec[bskey][bidx]["buy"]/cur_rec["total_money"])));
		col_idx=col_idx+1;ws.write(row_idx, col_idx, cur_rec[bskey][bidx]["sell"], green_format);
		col_idx=col_idx+1;ws.write(row_idx, col_idx, float("%.02f"%(cur_rec[bskey][bidx]["sell"]/cur_rec["total_money"])));

		diff = float(cur_rec[bskey][bidx]["buy"]) - float(cur_rec[bskey][bidx]["sell"])
		if diff > 0:
			col_idx = col_idx + 1;ws.write(row_idx, col_idx, diff, red_format);
		else:
			col_idx = col_idx + 1;ws.write(row_idx, col_idx, diff, green_format);
			
#		col_idx = col_idx + 1;ws.write(row_idx, col_idx, cur_rec["notion"].decode("utf-8"));
		col_idx = col_idx + 1;common_api.xlsxwriter_write_chinese(ws,row_idx, col_idx, re_target[1]);
		col_idx = col_idx + 1;common_api.xlsxwriter_write_chinese(ws,row_idx,col_idx,cur_rec["notion"]);
		row_idx = row_idx + 1;
	return row_idx;


def excel_do_gen():
	g_rec=common_api.g_rec;

	wb = xlsxwriter.Workbook("out.xlsx")
	date_format = wb.add_format({'num_format': 'yyyy-m-d','align': 'center'})
	#format:
	header_format = wb.add_format({'bold': True,
		'align': 'center',
		'valign': 'vcenter',
		'fg_color': '#D7E4BC',
		'border': 1})
	ws = wb.add_worksheet("1")
	ws.freeze_panes(1,2)


	for col_idx in range(len(heads)):
		#print heads[col_idx]
		#print type(heads[col_idx])
		#print type(heads[col_idx].encode("utf-8"))
		ws.write(0, col_idx, heads[col_idx], header_format);
	
	ws.set_column(1, 1, 12);#name
	ws.set_column(3, 3, 50);#who
	ws.set_column(9, 9, 15);#who
	row_idx=1;
	for key in g_rec.keys():
		#print key
		cur_rec=g_rec[key][0]
		#print cur_rec
		#print cur_rec[keys[1]]

		row_idx=excel_gen_all_list_in_record(wb, ws, cur_rec, "buy", row_idx)
		row_idx=excel_gen_all_list_in_record(wb, ws, cur_rec, "sell", row_idx)

	#ws.data_validation(1,1,100,1, {'validate': 'date'});
	wb.close();
