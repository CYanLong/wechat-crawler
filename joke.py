import requests
from scrapy.selector import Selector

import logging

url = "http://www.qiushibaike.com/hot/"
#r = requests.get(url)

def getjoke():
	
	r = requests.get(url)
	with open('j.html', 'w', encoding='utf-8') as f:
		f.write(r.content.decode('utf-8'))
	
	li_se = Selector(text=r.content.decode('utf-8')).xpath('//div[@id="content-left"]/div[@class="article block untagged mb15"]/div[@class="content"]/text()').extract()[:3]
	li_se = [li for li in li_se if li.split(" ") != ""]
	return "\n".join(li_se)
	#print(str(li_se).encode('utf-8'))
	
#getjoke()

#with open('joke.html', 'w', encoding='utf-8') as f:
#	f.write(r.content.decode('utf-8'))
