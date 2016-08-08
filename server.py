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
from crawler import get_news
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
    '''process message
    '''
    req_xml = etree.fromstring(request.data) #..XML.
    logging.info(etree.tostring(req_xml, pretty_print=True).decode())

    content = get_news(2)
    resp_xml = resp_message(req_xml, content)
    
    loggine.info(etree.tostring(root, pretty_print=True).decode())
    
    return Response(etree.tostring(resp_xml), mimetype = 'text/xml') 


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)

