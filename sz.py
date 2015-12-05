# -*- coding: utf-8 -*-
import time
import datetime
import common_api
import stock_notion_keeper


def sz_gen_record_from_data(data):
	start_flag=0;
	cur_reason=0;
	cur_date=None
	for i in range(len(data)):
		cur_line = data[i];
		print cur_line;
		if cur_line.find("年") != -1 and cur_line.find("日") != -1 and cur_line.find("月") != -1:
			dformat="(%Y年%m月%d日)"
			cur_date = datetime.datetime.strptime(cur_line.strip(), dformat);
		if cur_line.find("详细信息") != -1:
			start_flag = 1;
		if start_flag == 0:
			continue;
		if cur_line.find("日涨幅偏离值达到7%的前五只证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("日跌幅偏离值达到7%的前五只证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("日振幅值达到15%的前五只证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("日换手率达到20%的前五只证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("无价格涨跌幅限制的证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("连续三个交易日内，涨幅偏离值累计达到20%的证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("连续三个交易日内，跌幅偏离值累计达到20%的证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("连续三个交易日内，涨幅偏离值累计达到12%的ST证券、*ST证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("连续三个交易日内，跌幅偏离值累计达到12%的ST证券、*ST证券") != -1:
			cur_reason = cur_reason+1;
		elif cur_line.find("其它异常波动的证券") != -1:
			break;
		print cur_reason;
	
		if cur_line.find("(代码") != -1:
			name=common_api.str_get_str_between(cur_line,"","(代码");
			code=common_api.str_get_str_between(cur_line,"(代码",")");
			total_mon=common_api.str_get_str_between(cur_line,"成交金额:","万元");
			print name
			print code;
			print total_mon;
			notion=stock_notion_keeper.stock_get_notion(code);
			#gen init record:
			cur_rec = common_api.record_gen_and_init(code, name, cur_date, cur_reason, float("%.2f" %(float(total_mon)*10000/common_api.base_money)), notion);
		
			j=i;
			bslist_start = 0;
			while bslist_start != 1:
				new_line = data[j];
				if new_line.find("买入金额最大的前5名") != -1:
					bslist_start = 1;
					break;
				j = j+1;
			for idx in range(5):
				msg_line = data[j+idx+3];
				if len(msg_line) < 5:
					break;
				who=msg_line.split()[0]
				buy=msg_line.split()[1]
				sell=msg_line.split()[2]
				common_api.record_add_one_list(cur_rec, "buy", who, float("%.2f" %(float(buy)/common_api.base_money)), float("%.2f" %(float(sell)/common_api.base_money)));
		
			bslist_start = 0;
			while bslist_start != 1:
				new_line = data[j];
				if new_line.find("卖出金额最大的前5名") != -1:
					bslist_start = 1;
					break;
				j = j+1;
			for idx in range(5):
				msg_line = data[j+idx+3]
				if len(msg_line) < 5:
					break;
				who=msg_line.split()[0]
				buy=msg_line.split()[1]
				sell=msg_line.split()[2]
				common_api.record_add_one_list(cur_rec, "sell", who, float("%.2f" %(float(buy)/common_api.base_money)), float("%.2f" %(float(sell)/common_api.base_money)));
			common_api.record_join_to_global(cur_rec)
	
