#-*- conding: utf-8 -*-

'''
	author: cyanlong
	data: 2016-08-13
'''
from flask import Flask
from flask import request
from flask import Response
import requests
from xml.etree import ElementTree
from lxml import etree
import time
import hashlib
import operator

from xmlutils import respMessage
from xmlutils import respMedia
from xmlutils import respImageAndText

from joke import joke
from douban import getMovieBySub
from douban import getMovieByName
from douban import movieByTag

import retrieve

import logging

logging.basicConfig(
	filename = 'app.log',
	level=logging.INFO
	)

app = Flask(__name__)

@app.route('/', methods = {'GET'})
def checkSignature():
    '''token verification
    '''
    return request.args.get('echostr')

@app.route('/', methods = {'POST'})
def pro_message():
	'''
	接收并分析消息,调用对应的模块获取到数据并回应.
	'''

	req_xml = etree.fromstring(request.data)
	#接收到的短信息
	logging.info('new request: %s', etree.tostring(req_xml, pretty_print=True, encoding='utf-8'))
	
	uid = req_xml.find('FromUserName')
	#首先得到消息类型.
	mesType = req_xml.find('MsgType').text
	
	#如果是图片,原样返回图片
	if mesType  == 'image':
		return resp(respMedia(req_xml))
	
	guide = """以下是本订阅号的使用指南:\n 
			1:回复 书籍检索/书籍/检索 书名 得到黑大图书馆藏信息\n
			2:回复 段子 可得到一条笑话\n\n  
			3:回复 电影推荐 可得到一部电影 
			也可在后面加一个电影类型 例如: 电影推荐 剧情 
			(类型可以是豆瓣电影支持的任何类型,
			例如:爱情, 喜剧, 经典, 情色, 同志... 等,详见:https://movie.douban.com/tag/) 可得到一部关于此分类的电影 
			4:回复 电影 电影名 可得到关于此电影的详细信息.(来源于豆瓣)"""

	#处理新的关注和不再关注
	if mesType == 'event':
		event = req_xml.find('Event').text
		if event == 'subscribe': #新的关注
			content = '谢谢关注! 萌萌哒.\n' + guide
			return resp(respMessage(req_xml, content))
		elif event == "unsubscribe":
			content = ""
			return resp(respMessage(req_xml, content))
	
	#解析文本消息
	li_mess = req_xml.find('Content').text.split(" ")
	li_mess = [ s for s in li_mess if s != " "]

	size = len(li_mess)
	
	if size == 1:
		key = li_mess[0]
		if "段子" in key :
			uid = req_xml.find('FromUserName').text
			content = joke(uid)
			return resp(respMessage(req_xml, content))

	elif size == 2:
		key, value = li_mess[0], li_mess[1]

		if "书" in key or "检" in key:
			book_name = value
			logging.info("book name: %s" % book_name)
			return resp(respMessage(req_xml, retrieve.search(book_name)))
		elif "电影推荐" in key:
			uid = req_xml.find('FromUserName').text
			logging.debug(uid)
			title, desc, picUrl = movieByTag(uid, value)
			return resp(respImageAndText(req_xml,title, desc, picUrl))
		elif "电影" in key:
			title, desc, picUrl = getMovieByName(value)
			return resp(respImageAndText(req_xml, title, desc, picUrl))
	
	content = '输入错误!\n' + guide
	respXml = respMessage(req_xml, content)
	logging.info('resp: %s', etree.tostring(respXml, pretty_print=True))
	
	return Response(etree.tostring(respXml,encoding='utf-8'), mimetype = 'text/xml;charset=utf-8') 


def resp(respXml):
	'''将xml消息发送出去
	'''
	logging.info('resp: %s' etree.tostring(respXml, pretty_print=True))
	return Response(etree.tostring(respXml, encoding='utf-8'), mimetype='text/xml;charset=utf-8')


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80)

