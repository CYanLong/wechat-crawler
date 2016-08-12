#-*- encoding=utf-8 -*-
import time
import chardet
from lxml import etree
import logging

def resp_message(req_xml, content_str):
	
	
	resp_xml = etree.Element('xml')
    
	toUserName = etree.SubElement(resp_xml, "ToUserName")
	
	toUserName.text = etree.CDATA(req_xml.find('FromUserName').text)
	
	fromUserName = etree.SubElement(resp_xml, "FromUserName")
	
	fromUserName.text = etree.CDATA(req_xml.find('ToUserName').text)
	
	createTime = etree.SubElement(resp_xml, 'CreateTime')
	
	createTime.text = str(int(time.time()))
	
	msgType = etree.SubElement(resp_xml, 'MsgType')
	
	msgType.text = etree.CDATA(req_xml.find('MsgType').text)
	
	content = etree.SubElement(resp_xml, 'Content')
	#logging.info("======content charset: %s ======" % chardet.detect(content_str)['encoding'])
	content.text = etree.CDATA(content_str)
	
	return resp_xml


def resp_imageAndText(req_xml, title, desc, picUrl):
	resp_xml = etree.Element('xml')
	toUserName = etree.SubElement(resp_xml, 'ToUserName')
	toUserName.text = etree.CDATA(req_xml.find('FromUserName').text)

	fromUserName = etree.SubElement(resp_xml, 'FromUserName')
	fromUserName.text = etree.CDATA(req_xml.find('ToUserName').text)

	createTime = etree.SubElement(resp_xml, 'CreateTime')
	createTime.text = etree.CDATA(str(int(time.time())))
	
	etree.SubElement(resp_xml, 'MsgType').text = etree.CDATA('news')

	etree.SubElement(resp_xml, 'ArticleCount').text = '1'

	articles = etree.SubElement(resp_xml, 'Articles')
	item = etree.SubElement(articles, 'item')
	etree.SubElement(item, 'Title').text = title
	etree.SubElement(item, 'Description').text = desc
	etree.SubElement(item, 'PicUrl').text = picUrl
	
	return resp_xml

def resp_media(req_xml):
	resp_xml = etree.Element('xml')
	toUserName = etree.SubElement(resp_xml, "ToUserName")
	toUserName.text = etree.CDATA(req_xml.find('FromUserName').text)
	fromUserName = etree.SubElement(resp_xml,"FromUserName")
	fromUserName.text = etree.CDATA(req_xml.find('ToUserName').text)

	createTime = etree.SubElement(resp_xml, "CreateTime")
	createTime.text = str(int(time.time()))

	msgType = etree.SubElement(resp_xml, 'MsgType')
	msgType.text = etree.CDATA(req_xml.find('MsgType').text)
	
	image = etree.SubElement(resp_xml, 'Image')
	mediaId = etree.SubElement(image, 'MediaId')
	mediaId.text = etree.CDATA(req_xml.find('MediaId').text)

	return resp_xml
