#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
	author: cyanlong
	data: 2016-08-13

'''

import requests
import json
from scrapy.selector import Selector
import sqlite3
import logging

from sql import start_num

logging.basicConfig(level=logging.DEBUG)

def getDataById(mid):
	'''根据电影id得到电影的详细描述信息:title, desc picUrl

	'''
	itemUrl = 'https://api.douban.com/v2/movie/' + mid
	
	itemJson = requests.get(itemUrl)
	
	itemData = json.loads(itemJson.content.decode('utf-8'))
	#得到json数据,解析并拼接返回结果.
	rate = itemData['rating']['average'] #评分
	numRaters = itemData['rating']['numRaters'] #评论人数
	li_cast = itemData['attrs']['cast']
	n = len(li_cast)
	n = 3 if n > 3 else n 
	casts = " ".join(li_cast[:n])
	#描述
	def desc_str():
		yield '\n\n原名: ' + itemData['title'] 
		yield '\n\n豆瓣评分: ' + str(itemData['rating']['average']) + '(' + str(itemData['rating']['numRaters']) + '人评)' 
		yield '\n\n导演:' + itemData['author'][0]['name'] + '\n\n主演:' + casts
		yield '\n\n剧情简介: ' + itemData['summary']
		yield '\n\n豆瓣链接:' + itemUrl
	desc = ''.join(desc_str())
	title = itemData['alt_title']
	picUrl = itemData['image']
	return title, desc, picUrl

def getMovieBySub(start, tag="经典"):
	''' 根据一个page_start值和分类值tag得到一个电影信息
	'''
	
	req_param = {
		"type": "movie",
		"tag": tag,
		"sort": "rank",
		"page_limit": 1,
		"page_start": start
	}
	
	sub_url = 'https://movie.douban.com/j/search_subjects'

	resp = requests.get(sub_url, params = req_param)
	
	li = json.loads(resp.content.decode('utf-8'))['subjects']
	
	item = li[0]
	
	itemUrl = item['url']
	#电影的id
	mid = itemUrl.split('/')[-2]
	
	return getDataById(mid)

def getMovieByName(movieName):
	'''根据电影名得到电影详细信息,首先得到mid,调用getDataById得到详细信息
	'''
	search_url = 'https://movie.douban.com/subject_search?search_text=' + movieName
	
	resp = requests.get(search_url)

	items = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="article"]/div/table[@width="100%"]/tr[@class="item"]/td[@valign="top"]/a/@href').extract()
	
	if len(items) == 0:
		return "无法找到"
	
	else:
		#只取第一项
		mid = items[0].split('/')[-2]
		
		return getDataById(mid)


def movieByTag(userId, tag="经典"):
	''' 根据不同的用户返回不同的信息
	'''
	
	start = start_num(userId, tag)
	
	return getMovieBySub(start, tag)


if __name__ == '__main__':
	'''测试
	'''
	print(getMovieBySub(1, tag="同性"))
