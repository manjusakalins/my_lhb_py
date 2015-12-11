# -*- coding: utf-8 -*-
import time
import datetime
import common_api
import stock_notion_keeper

base_money = common_api.base_money
def sh_gen_record_from(file_lines):
	tstart = time.clock()
	if file_lines == None:
		return;
	cur_reason=0;
	g_total_money={};
	for i in range(len(file_lines)):
		cur_line = file_lines[i];
		#print cur_line


		if cur_line.find(u"一、有价格涨跌幅限制的日收盘价格涨幅偏离值达到7%的前三只证券") != -1:
			cur_reason="+7%";
		elif cur_line.find(u"二、有价格涨跌幅限制的日收盘价格跌幅偏离值达到7%的前三只证券") != -1:
			cur_reason="-7%";
		elif cur_line.find(u"三、有价格涨跌幅限制的日价格振幅达到15%的前三只证券") != -1:
			cur_reason="+-15%";
		elif cur_line.find(u"四、有价格涨跌幅限制的日换手率达到20%的前三只证券") != -1:
			cur_reason="c20%";
		elif cur_line.find(u"五、无价格涨跌幅限制的证券") != -1:
			cur_reason="none";
		elif cur_line.find(u"六、非ST、*ST和S证券连续三个交易日内收盘价格涨幅偏离值累计达到20%的证券") != -1:
			cur_reason="3+20%";
		elif cur_line.find(u"七、非ST、*ST和S证券连续三个交易日内收盘价格跌幅偏离值累计达到20%的证券:") != -1:
			cur_reason="3-20%";
		elif cur_line.find(u"八、ST、*ST和S证券连续三个交易日内收盘价格涨幅偏离值累计达到15%的证券") != -1:
			cur_reason="3+15%";
			break;
		elif cur_line.find(u"九、ST、*ST和S证券连续三个交易日内收盘价格跌幅偏离值累计达到15%的证券") != -1:
			cur_reason="3-15%";
		elif cur_line.find(u"十、") != -1:
			break;
		#print cur_reason;
		cur_str=cur_line.encode('utf-8')
		
		#get date
		if cur_str.find("年") != -1 and cur_str.find("日") != -1 and cur_str.find("月") != -1:
			dformat="交易日期:%Y年%m月%d日"
			cur_date = datetime.datetime.strptime(cur_str.strip(),dformat);
	
		#get totalmoney:
		if cur_str.find("成交量") != -1 and cur_str.find("成交金额") != -1:
			headlist=cur_str.split();
			cj_idx=5;
			for iii in range(len(headlist)):
				if headlist[iii].find("成交金额") != -1:
					cj_idx=iii;
			ttidx=i+1;
			while file_lines[ttidx].find("(") != -1 and file_lines[ttidx].find(")") != -1:
				cur_list = file_lines[ttidx].split();
				#print file_lines[ttidx]
				#print cur_list[5]
				#print cur_list
				if len(cur_list) < 6:
					g_total_money[str(cur_list[1])] = base_money;
					ttidx = ttidx+1;
					continue;
				g_total_money[str(cur_list[1])] = cur_list[cj_idx];
				ttidx = ttidx+1;
			#print g_total_money
				
		#get one record:
		if cur_str.find("证券代码:") != -1 and cur_str.find("证券简称") != -1:
			code=cur_str.split("证券代码:")[1].split("证券简称:")[0].strip()
			name=cur_str.split("证券代码:")[1].split("证券简称:")[1].strip()
			#print code
			#print name;
			notion=stock_notion_keeper.stock_get_notion(code);
			cur_rec = common_api.record_gen_and_init(code, name, cur_date, cur_reason, float("%.2f" %(float(g_total_money[code])*10000/base_money)), notion);

			#process buy.
			for j in range(5):
				cur_str=file_lines[i+3+j].encode('utf-8')
				#print cur_str.split();
				if len(cur_str) < 3 or cur_str.find("(") == -1:
					break;
				who=cur_str.split()[1];
				money=cur_str.split()[2];
				common_api.record_add_one_list(cur_rec, "buy", who, float("%.2f" %(float(money)/base_money)), float("0.0"));
		
			#process sell
			for j in range(5):
				cur_str=file_lines[i+3+5+2+j].encode('utf-8')
				if len(cur_str) < 3 or cur_str.find("(") == -1:
					break;
				who=cur_str.split()[1];
				money=cur_str.split()[2];
				common_api.record_add_one_list(cur_rec, "sell", who, float("0.0"), float("%.2f" %(float(money)/base_money)));
			common_api.record_join_to_global(cur_rec)
	tend = time.clock()
	#print "run time %.2gs" % (tend-tstart)
