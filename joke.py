#-*- conding:utf-8 -*-

'''
	author: cyanlong
	data: 2016-08-13
'''

import requests
from scrapy.selector import Selector
from sql import start_num

import logging

url = "http://www.qiushibaike.com/hot/page/2/"

def joke(uid):
	'''随机得到一条笑话'''	
	
	params = {
		's': '4903577'
	}
	
	r = requests.get(url, params)
	
	num = start_num(uid, '段子')
	num = num + 1
	num = str(num)
	li_se = Selector(text=r.content.decode('utf-8')).xpath('string((//div[@id="content-left"]/div[@class="article block untagged mb15"]/div[@class="content"])['+num+'])').extract()
	
	return "\n".join(li_se)


if __name__ == '__main__':
	joke('123')
