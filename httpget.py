#coding:utf-8
import os
import requests
import sys 
import io
from lxml import etree
import time

#url------------------------------------------------------------
main_url = "https://tools.pediy.com/"

#xpath定义------------------------------------------------------
#平台标题
xp_platform_title = "/html/body/div[2]/div/div[1]/div[@class='tit']/h2"
#平台内容
xp_platform_content = "/html/body/div[2]/div/div[1]/div[%d]/a/%s"


#头
headers = {
	'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
}

def GetMainMenu():
	r = requests.get(main_url, headers=headers)
	if (r.status_code != 200):
		print("访问失败,错误码: %d" % r.status_code)
		print(r.text)
		exit()

	# fo = open("test.html", "w", encoding=r.encoding)
	# fo.write(r.text)
	# fo.close()
	# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=r.encoding)

	#html文本
	str_html = r.text.encode(r.encoding).decode("utf-8")

	#html解析
	html = etree.HTML(str_html)

	#页面数据对象
	obj_page = {}

	#大标题
	titles = []
	for i in html.xpath(xp_platform_title):
		titles.append(i.text)
		print(i.text)
	obj_page['titles'] = titles

	#子标题
	contents = []
	for i in range(1, len(titles)+1):
		obj = {}
		tlts = []
		#标题
		for j in html.xpath(xp_platform_content % ((i * 2), "text()")):
			tlts.append(j)
		obj['titles'] = tlts

		#url
		urls = []
		for j in html.xpath(xp_platform_content % ((i * 2), "@href")):
			urls.append(j)
		obj['urls'] = urls

		contents.append(obj)

	obj_page['contents'] = contents
	print(obj_page)
	return obj_page

def GetTools(url):

	print("\n")
	tmp = url[:url.find('/')]

	xp_col1 = "//div[@class='con']//table//tr/td[1]//a[@href]"
	xp_col2 = "//div[@class='con']//table//tr/td[2]//text()"
	xp_col3 = "//div[@class='con']//table//tr/td[3]"

	r = requests.get(main_url + url, headers=headers)
	if (r.status_code != 200):
		print("访问失败,错误码: %d" % r.status_code)
		print(r.text)
		return {}

	#html文本
	str_html = r.text.encode(r.encoding).decode("utf-8")

	#html解析
	html = etree.HTML(str_html)

	# fo = open("test.html", "w", encoding="utf-8")
	# fo.write(str_html)
	# fo.close()

	obj_tools = {}

	colums1_titles = []
	for i in html.xpath(xp_col1):
		if i != "":
			colums1_titles.append(str(i.text).strip())

	colums1_urls = []
	for i in html.xpath(xp_col1 + "/@href"):
		colums1_urls.append(main_url + tmp + "/" + i)

	authors = []
	for i in html.xpath(xp_col2):
		authors.append(i)

	descriptors = []
	for i in html.xpath(xp_col3):
		str_tmp = str(i.text)
		for j in i:
			if j.text == None:
				str_tmp += str(j.tail)
			else:
				str_tmp += str(j.text)
		descriptors.append(str_tmp)

	obj_tools['colums1_titles'] = colums1_titles
	obj_tools['colums1_urls'] = colums1_urls
	obj_tools['authors'] = authors
	obj_tools['descriptors'] = descriptors
	return obj_tools

def downloadFile(name, url, caller=None):
	headers = {
		'Proxy-Connection':'keep-alive',
		'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
	}
	r = requests.get(url, stream=True, headers=headers)
	if (r.status_code != 200):
		print(r.status_code)
		return { "status" : False , 'msg' : "下载失败,错误代码: %d" % r.status_code}

	length = float(r.headers['content-length'])
	f = open(name, 'wb')
	count = 0
	count_tmp = 0
	time1 = time.time()
	for chunk in r.iter_content(chunk_size = 512):
		if chunk:
			f.write(chunk)
			count += len(chunk)
			if time.time() - time1 > 2:
				p = count / length * 100
				speed = (count - count_tmp) / 1024 / 1024 / 2
				count_tmp = count
				# print(name + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'M/S')
				time1 = time.time()
				if (caller != None):
					caller(p, speed)
	f.close()
	return { "status" : True , 'msg' : "ok"}
    
def formatFloat(num):
    return '{:.2f}'.format(num)