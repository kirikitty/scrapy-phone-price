# -*- coding: utf-8 -*-
import re

def isnumber(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

replaced_keywords_initialized = False
replaced_keywords = []
def create_replaced_keywords():
	global replaced_keywords_initialized
	global replaced_keywords
	replaced_keywords_initialized = True
	kvs = {}
	# kvs['motorola'] = '摩托罗拉'
	# kvs['Nokia'] = '诺基亚'
	kvs['GIONEE'] = '金立'
	kvs['Coolpad'] = '酷派'
	kvs['Hisense'] = '海信'
	kvs['HONOR'] = '荣耀'
	kvs['HUAWEI'] = '华为'
	kvs['LeEco'] = '乐视'
	kvs['Letv'] = '乐视'
	kvs['Lenovo'] = '联想'
	kvs['Meitu'] = '美图'
	kvs['Meizu'] = '魅族'
	kvs['OnePlus'] = '一加'
	kvs['SMARTISAN'] = '锤子'
	kvs['Xiaomi'] = '小米'
	kvs['Redmi'] = '红米'

	keywords = []
	for (k,v) in kvs.items():
		keywords.append({'re': re.compile(k, re.IGNORECASE), 'to': v})
	replaced_keywords = keywords

def replace_keyword(keyword):
	global replaced_keywords_initialized
	global replaced_keywords

	if not replaced_keywords_initialized:
		create_replaced_keywords()

	s = keyword
	for rk in replaced_keywords:
		s = re.sub(rk['re'], rk['to'], s)
	return s
