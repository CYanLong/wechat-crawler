from flask import Flask
from flask import request
import hashlib
import operator
from xml.dom.minidom import Document
from xml.etree import ElementTree
from lxml import etree
from flask import Response
import time

app = Flask(__name__)

@app.route('/', methods = {'GET'})
def checkSignature():
    print('--get method--')
    print(request.data)
    return request.args.get('echostr')

@app.route('/', methods = {'POST'})
def pro_message():
    print('--post--')
    str_xml = request.data
    xml = etree.fromstring(str_xml) #..XML.
    print(etree.tostring(xml, pretty_print=True).decode())
    content = xml.find('Content').text.encode('utf-8')
    msgType = xml.find('MsgType').text.encode('utf-8')
    print("Content: %s, msgType: %s" % (content, msgType))


    root = etree.Element('xml')
    toUserName = etree.SubElement(root, "ToUserName")
    toUserName.text = etree.CDATA(xml.find('FromUserName').text)

    fromUserName = etree.SubElement(root, "FromUserName")
    fromUserName.text = etree.CDATA(xml.find('ToUserName').text)

    createTime = etree.SubElement(root, 'CreateTime')
    createTime.text = str(int(time.time()))
    
    msgType = etree.SubElement(root, 'MsgType')
    msgType.text = etree.CDATA(xml.find('MsgType').text)
    
    content = etree.SubElement(root, 'Content')
    content.text = etree.CDATA('lalal')
    
    print(etree.tostring(root,pretty_print=True).decode())
    return Response(etree.tostring(root), mimetype = 'text/xml') 


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)

