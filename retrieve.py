#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	author: cyanlong
	data: 2016-08-13
'''

import requests
from scrapy.selector import Selector
import logging

logging.basicConfig(level=logging.INFO)

search_url = 'http://210.46.107.77:8080/opac/search'
root_url = 'http://210.46.107.77:8080'
def search(q):
	'''根据书名检索馆藏信息
	'''
	
	fdata = {
		'tag': 'search',
		'subtag': 'simsearch',
		'gcbook': 'yes',
		'viewtype': '',
		'flword': '',
		'viewtype': '',
		'q': q
	}
	
	resp = requests.post(search_url, data=fdata)
	#得到记录条数
	s_res = Selector(text=resp.content.decode('utf-8')).xpath('//p[@id="page"]/span/text()')
	#如没有检索到记录,result_list为空
	result_list = s_res.extract()
	if len(result_list) == 0:
		return "没有检索到记录"
	result_str = result_list[0]
	num = int(s_res.re('[\d]+')[0])
	
	if num > 3:
		note = ""
		if num > 10:
			note = "\n注:只显示前10条结果,得到所有检索结果:" +  search_url + "\n======"
		return result_str + "\n======" + note + getManyLinks(resp, num)
	else:
		return result_str + "\n======" + getdetail(resp, num)


def getdetail(resp, num):
	'''记录小于等于3条,返回详细信息
	'''	
	
	se = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="jp-booksInfo"]')
	li_author = se.xpath('.//p[@class="creator"]/a/text()').extract()
	li_call_number = se.xpath('.//p[@class="call_number"]/text()').extract()
	li_publisher = se.xpath('.//p[@class="publisher"]/text()').extract()
	li_h_se = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="jp-searchList"]/ul/li/h2/a')
	
	li_href = li_h_se.xpath('.//@href').extract()

	li_bname =li_h_se.xpath('.//text()').extract()

	items = []
	for i in range(0, num):
		author = li_author[i].strip()
		call_number = li_call_number[2*i+1]
		publisher = li_publisher[i].strip()
		href = li_href[i]
		bid = href.split('/')[-1]
		bname = li_bname[i]
		summer, has = getBookState(bid)	

		bname = "\n " + bname
		author = "\n " + author
		publisher = "\n " + publisher 
		call_number = "\n 索书号:" + call_number
		summer = "\n 馆藏数:" + summer
		has = "\n 可借数:" + has

		link = "\n 详细信息:"  + root_url + href
		content = bname + author + publisher + call_number + summer + has + link
		items.append(content)
	return "\n=======".join(items)

#记录大于等于三条,只返回前10条详细链接
def getManyLinks(resp, num):
	'''记录大于3条,只返回前10条链接
	'''
	num = 10 if num > 10 else num
	
	li_bname = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="jp-searchList"]/ul/li/h2/a/text()').extract()

	li_href = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="jp-searchList"]/ul/li/h2/a/@href').extract()[0: num]
	li_link = [root_url + href for href in li_href]
	li_publisher = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="jp-booksInfo"]/p[@class="publisher"]/text()').extract()
	
	items = []
	for i in range(0, num):
		name = '\n书名:' + li_bname[i]
		publisher = "\n出版社:" + li_publisher[2*i + 1]
		content = "\n详细信息:" + li_link[i]		
		items.append(name + publisher + content)
	
	return "\n======".join(items)


def getBookState(bid):
	
	url = "http://210.46.107.77:8080/opac/book/getBookState/"+bid+"/%E5%9B%BE%E4%B9%A6"

	r = requests.get(url)

	li = r.content.decode('utf-8').split('/')
	return li[0], li[1]

if __name__ == '__main__':
	'''测试'''
	#print(search('红与黑'))
