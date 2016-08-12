#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


pn = 0
rn = 1

url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=斗图表情包&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&word=斗图表情包&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&pn="+pn+"&rn="+rn+"&gsm=1e&1470889154331="

r = requests.get(url)

j = r.json()

j

#with open("emoticon.html", 'w', encoding='utf-8') as f :
#	f.write(r.content.decode('utf-8'))
