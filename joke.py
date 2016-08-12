import requests
from scrapy.selector import Selector

import logging

url = "http://www.qiushibaike.com/hot/"

def getjoke():
	'''随机得到一条笑话'''	
	r = requests.get(url)
	
	li_se = Selector(text=r.content.decode('utf-8')).xpath('//div[@id="content-left"]/div[@class="article block untagged mb15"]/div[@class="content"]/text()').extract()[:3]
	li_se = [li for li in li_se if li.split(" ") != ""]
	return "\n".join(li_se)
	
if __name__ == '__main__':
	getjoke()