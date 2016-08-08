from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests
import logging
logging.basicConfig(level=logging.INFO)

root_url = "http://xyw.hlju.edu.cn/"
def get_news(num):
	'''得到num条校内通知.
	'''
	resp = requests.get(root_url)
	logging.info("index page: %s" % resp.status_code)
	
	newsbox = Selector(text=resp.content.decode('utf-8')).xpath('//div[@class="newsbox fleft"]')
	#得到所有通知的链接
	links = newsbox.xpath('.//li/a/@href').extract()
	logging.info("links: %s" % links)
	
	items = pro_links(links)
	num = min(num, len(items))
	items = items[:num]
	li = []	
	for item in items:
		#logging.info("%s %s" % (item['title'], item['date']))
		li.append("%s%s" % (item['title'], item['date']))
	content = "\n".join(li)
	logging.info(content)
	return content


def pro_links(links):
	'''追踪每个消息内容页,返回每一对date和title的集合
	'''
	items = []

	for link in links:
		link = root_url + link
		resp = requests.get(link)
		logging.info("content page: %s" % resp.status_code)
		if resp.status_code != 200:
			continue
		se = Selector(text=resp.content.decode('utf-8'))
		title = se.xpath('//td[@class="titlestyle122328"]/text()').extract()
		date = se.xpath('//span[@class="timestyle122328"]/text()').extract()
		#logging.info("title:%s, date: %s" % (title, date))
		item = {"title": title[0], "date": date[0]}
		#logging.info(item)
		items.append(item)

	return items


if __name__ == '__main__':
	get_news(5)


#dates = newsbox.xpath('.//li/span/text()').extract()
	#titles = newsbox.xpath('.//li/a/text()').extract()num