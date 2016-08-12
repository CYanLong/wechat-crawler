#-*-utf-8-*-
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests
import logging
import os
from PIL import Image
import pytesseract
from urllib import request

logging.basicConfig(level=logging.INFO)


root_url = "http://xyw.hlju.edu.cn/"
def get_news(num, iplent):
	#root_url = "http://xyw.hlju.edu.cn/"
	header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		  "Accept-Language": " zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		  "Accept-Encoding": "gzip, deflate",
		  "Connection": "keek-alive",
		  #"Host": "xyw.hlju.edu.cn",
		  #"Referer": "http://web.hlju.edu.cn:8080/system/resource/code/auth/ipauth.jsp",
		  #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
		  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
		  "Cookie": iplent
		  }
	pdata = "casloginaction=login&casloginuser=20146219"

	exist = os.path.isfile('index.html')

	
	#if exist==True:
	#	with open('index.html', 'r', encoding='utf-8') as f:
	#		data = f.read()
	#else:
	resp = requests.post(root_url, headers = header, data = pdata, allow_redirects=False)
	#data = resp.content.decode('utf-8')
	#with open('index.html', 'w', encoding='utf-8') as f:
	#	f.write(resp.content.decode('utf-8'))
	logging.info(resp.headers)
	logging.info(resp.status_code)
	
	loc_url = resp.headers['Location']
	print(loc_url)
	re = requests.get(loc_url, headers = header, allow_redirects=False)
	print(re.headers)
	
	ll_url = re.headers['Location']
	print(ll_url)
	cookie = re.headers['Set-Cookie'].split(';')[0]
	ll_hread = {
		"Cookie": cookie
	}
	ree = requests.get(ll_url, headers = ll_hread, allow_redirects = False)
	print(ree.headers)
	#newsbox = Selector(text = data).xpath('//div[@class="newsbox fleft"]')
	#links = newsbox.xpath('.//li/a/@href').extract()
	#logging.info("links: %s" % links)
	#links = links[:num]
	#items = pro_links(links)
	#num = min(num, len(items))
	#items = items[:num]
	#li = []	
	#for item in items:
		#logging.info("%s %s" % (item['title'], item['date']))
	#    li.append("%s%s" % (item['title'], item['date']))
	#content = "\n".join(li)
	#logging.info(content)
	#return content


def pro_links(links):
	items = []

	for link in links:
		link = root_url + link
		resp = requests.get(link, headers = header)
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

#模拟登录
login_url = "http://my.hlju.edu.cn/userPasswordValidate.portal"
cap_url = "http://my.hlju.edu.cn/captchaGenerate.portal"
login_page = 'http://my.hlju.edu.cn'

	
#得到验证码
def get_code(cook):
	'''
	head = {
			"Proxy-Connection": "keep-alive",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
	}
	r_page = requests.get(login_page, headers = head)
	logging.info(r_page.status_code)
	logging.info('第一次访问page:')
	logging.info(r_page.headers)
	session_id = r_page.headers['Set-Cookie']	
	session_id = session_id.split(";")[0]
	header = {"Cookie": session_id,
			   "Referer": "http://my.hlju.edu.cn/login.portal",
			   "Host": "my.hlju.edu.cn"
			   }
	logging.info("session_id %s" % session_id)
	'''
	#请求capa
	r_cap = requests.get(cap_url)
	logging.info(r_cap.headers)
	with open("v.jpg", 'wb') as f:
		for chunk in r_cap:
			f.write(chunk)
	#session_id = r_cap.headers['Set-Cookie']
	print(session_id)
	code = pytesseract.image_to_string(Image.open('v.jpg'))
	logging.info("code %s" % code)
	if len(code) == 4:
		
		h = {'Cookie': session_id,
			"Proxy-Connection": "keep-alive",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
			"Referer": "http://my.hlju.edu.cn/login.portal"
			}
		r = requests.get("http://my.hlju.edu.cn/captchaValidate.portal?captcha="+code+"&what=captcha&value="+code+"&_=", headers = h)
		logging.info('验证 code....')
		print(r.headers)
		return code,session_id
	

def login(jsess_id, code):
	fdata = {
		"Login.Token1": "20146219",
		"Login.Token2": "745565148",
		"captcha": code,
		"goto": 'http://my.hlju.edu.cn',
		"gotoOnFail": "http://my.hlju.edu.cn/loginSuccess.portal"
	}

	he = {"Cookie": jsess_id}
	r_login = requests.post(login_url, headers = he, data=fdata)
	logging.info("login status: %s" % r_login )
	with open('login_success.html', 'w', encoding="utf-8") as f:
		f.write(r_login.content.decode('utf-8'))
	logging.info('登录成功')
	logging.info(r_login.headers)
	return r_login.headers['Set-Cookie'].split(';')[0]


def test():
	url = 'http://web.hlju.edu.cn:8080/system/resource/code/auth/ipauth.jsp'
	headers = {}
	r = requests.get(url)
	with open('ipauth.html', 'w', encoding='utf-8') as f:
		f.write(r.content.decode('utf-8'))
	print(r.headers)

def test2():
	with request.urlopen('http://xyw.hlju.edu.cn/') as f:
		data = f.read()
		print('Status:', f.status, f.reason)
		for k, v in f.getheaders():
			print('%s: %s' %(k, v))
		
		with open('index.html', 'w', encoding='utf-8') as f:
			f.write(data.decode('utf-8'))
		print('Data:', data.decode('utf-8'))

def test3():
	url = "http://xyw.hlju.edu.cn/list_nav.jsp?urltype=tree.TreeTempUrl&wbtreeid=1095"
	#with request.urlopen(url) as f:
	#	print('Status:', f.status, f.reason)
	#	for k, v in f.getheaders():
	#		print('%s: %s' % (k, v))
	r = requests.get(url, allow_redirects=False)
	cook = r.headers['Set-Cookie'].split(';')[0]
	print(cook)
	return cook
	#print(r.headers)

if __name__ == '__main__':
	cook = test3()

	#code, session_id = get_code()
	#iplent = login(cook, code)
	#print(iplent)
	get_news(2, cook)

