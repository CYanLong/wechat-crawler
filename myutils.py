#-*-utf-8-*-

def resp_message(req_xml, content):
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
    content.text = etree.CDATA(content)
    return resp_xml