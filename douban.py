#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import json



#根据分类得到电影信息
def getMovieBySub(tag="经典"):
	
	req_param = {
		"type": "movie",
		"tag": tag,
		"sort": "rank",
		"page_limit": 20,
		"page_start": 0
	}
	
	sub_url = 'https://movie.douban.com/j/search_subjects'

	resp = requests.get(sub_url, params = req_param)
	
	li = json.loads(resp.content.decode('utf-8'))['subjects']
	print(str(li).encode('utf-8'))
	item = li[0]
	#print(str(item).encode('utf-8'))
	item_url = item['url']
	#电影的id
	mid = item_url.split('/')[-2]
	
	return getDataById(mid)
	

def getDataById(mid):
	'''根据电影id得到电影的详细描述信息:title, desc picUrl

	'''
	itemUrl = 'https://api.douban.com/v2/movie/'
	item_json_url = item_json_url + mid
	
	item_json = requests.get(item_json_url)
	
	itemData = json.loads(item_json.content.decode('utf-8'))
	#得到json数据,解析并拼接返回结果.
	rate = itemData['rating']['average'] #评分
	numRaters = itemData['rating']['numRaters'] #评论人数
	#描述
	desc =  '\n原名: ' + itemData['title'] + '\n豆瓣评分: ' + str(itemData['rating']['average']) + '(' + str(itemData['rating']['numRaters']) +  '人评)' + '\n 剧情简介: ' + itemData['summary'] + '\n 豆瓣链接:' + item_url
	title = itemData['alt_title']
	picUrl = itemData['image']
	return title, desc, picUrl


def getMovieDetail(movieName):
	'''根据电影名得到电影详细信息,首先得到mid,调用getDataById得到详细信息
	'''
	search_url = 'https://movie.douban.com/subject_search?search_text=' + movieName
	
	resp = requests.get(search_url)

	items = Selector(text=resp.content.decode('utf-8')).xpath('//tr[@class="item"]/a/@href').extract()
	
	if len(items) == 0:
		return "无法找到"
	
	else:
		#只取第一项
		mid = items[0].split('/')[-2]
		return getDataById(mid)

#测试
if __name__ == '__main__':
	getMovieBySub("纪录片")
