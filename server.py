#-*_utf-8_*-


from flask import Flask
from flask import request
import hashlib
import operator
from xml.dom.minidom import Document
from xml.etree import ElementTree
from lxml import etree
from flask import Response
import time
from myutils import resp_message
from myutils import resp_media
from myutils import resp_imageAndText
import myutils
from crawler import get_news
from joke import getjoke
from douban import getMovie
import logging
import requests
import retrieve
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
	
	logging.info(etree.tostring(req_xml, pretty_print=True, encoding='utf-8'))
	
	#首先得到消息类型.
	mesType = req_xml.find('MsgType').text
	
	if mesType  == 'image':
		return 
	
	li_mess = req_xml.find('Content').text.split(" ")
	li_mess = [ s for s in li_mess if s != " "]
	
	#resp_xml = myutils.resp_imageAndText(req_xml)
	
	size = len(li_mess)

	if size == 1:
		key = li_mess[0]
		content = "不懂.."
		if "段子" in key :
			content = getjoke()

	elif size == 2:
		key, value = li_mess[0], li_mess[1]
		content = "不懂你在说什么!"
		if "书" in key or "检" in key:
			book_name = value
			logging.info("book name: %s" % book_name)
			content = retrieve.search(book_name)
		elif "电影推荐" in key:
			title, desc, picUrl = getMovie(value)
			resp_xml = resp_imageAndText(req_xml,title, desc, picUrl)

	#logging.info(content)
	
	#resp_xml = resp_message(req_xml, content)
	
	#logging.info("resp_xml_str %s" % etree.tostring(resp_xml, pretty_print=True))
	
	return Response(etree.tostring(resp_xml,encoding='utf-8'), mimetype = 'text/xml;charset=utf-8') 


if __name__ == '__main__':

	app.run(host = '0.0.0.0', port = 80)

