#-*- conding: utf-8 -*-

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

from joke import getjoke
from douban import getMovieBySub
from douban import getMovieByName

import retrieve

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/', methods = {'GET'})
def checkSignature():
    '''token verification
    '''
    return request.args.get('echostr')

@app.route('/', methods = {'POST'})
def pro_message():
	'''
	接收并分析消息,调用对应的模块获取到数据并返回.
	'''

	req_xml = etree.fromstring(request.data)
	#接收到的短信息
	logging.info(etree.tostring(req_xml, pretty_print=True, encoding='utf-8'))
	
	#首先得到消息类型.
	mesType = req_xml.find('MsgType').text
	
	#如果是图片,原样返回图片
	if mesType  == 'image':
		return respMedia(req_xml)

	#解析文本消息
	li_mess = req_xml.find('Content').text.split(" ")
	li_mess = [ s for s in li_mess if s != " "]

	size = len(li_mess)
	content = "..."
	if size == 1:
		key = li_mess[0]
		if "段子" in key :
			content = getjoke()

	elif size == 2:
		key, value = li_mess[0], li_mess[1]

		if "书" in key or "检" in key:
			book_name = value
			logging.info("book name: %s" % book_name)
			content = retrieve.search(book_name)
		elif "电影推荐" in key:
			title, desc, picUrl = getMovieBySub(value)
			resp_xml = respImageAndText(req_xml,title, desc, picUrl)
		elif "电影" in key:
			title, desc, picUrl = getMovieByName(value)
			resp_xml = respImageAndText(req_xml, title, desc, picUrl)

	#返回信息
	resp_xml = resp_message(req_xml, content)
	
	logging.info("resp_xml_str %s" % etree.tostring(resp_xml, pretty_print=True))
	
	return Response(etree.tostring(resp_xml,encoding='utf-8'), mimetype = 'text/xml;charset=utf-8') 


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80)

