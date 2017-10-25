# -*- coding: utf-8 -*-
import time
import requests
import urllib2
import urllib 
import cookielib
import re
############################若出现ip封禁则取消此注释代码#########################
# from selenium import webdriver
# driver=webdriver.Chrome()
############################若出现ip封禁则取消此注释代码#########################
fh = open("books.txt", 'w')

############################若出现ip封禁则取消此注释代码#########################
#  #cookie 处理
# cookiejar = cookielib.LWPCookieJar()#LWPCookieJar提供可读写操作的cookie文件,存储cookie对象  
# cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)  
# opener = urllib2.build_opener(cookieSupport, urllib2.HTTPHandler)  
# urllib2.install_opener(opener)#打开登陆页面 
# loginurl='https://www.douban.com/accounts/login'
# driver.get(loginurl) 
# username = raw_input('please enter the username: ')
# password = raw_input('please enter the password: ')
# SecretCode = raw_input('please enter the code: ')
# driver.find_element_by_name("captcha-solution").send_keys(SecretCode)     #输入用户名
# #driver.find_element_by_name("yhmc").clear()    #清除用户名输入框中的内容
# driver.find_element_by_name("form_email").send_keys(username)     #输入用户名
# #driver.find_element_by_name("yhmm").clear()    #清除用户名输入框中的内容
# driver.find_element_by_name("form_password").send_keys(password)     #输入用户名
# driver.find_element_by_name("login").click()     #输入用户名
# cookie= driver.get_cookies()
# cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
# cookiestr = ';'.join(item for item in cookie)
# print cookiestr
############################若出现ip封禁则取消此注释代码#########################


headers={
############################若出现ip封禁则取消此注释代码#########################
	#'Cookie':cookiestr,
############################若出现ip封禁则取消此注释代码#########################
	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

def getBookList(BookType,PageIndex):
	links=[]
	url="https://book.douban.com/tag/"+BookType+"?start="+str(PageIndex*20)+"&type=T"
	req=urllib2.Request(url,headers = headers) 
	#获得服务器返回的数据  
	response = urllib2.urlopen(req)
	#处理数据  
	page=response.read()
	BookHerf= re.findall(r' <a class="nbg" href="(.+?)"', page)	
	for i in BookHerf:
		links.append(i.decode())
	return links


def getBookInfo(url):
	req=urllib2.Request(url,headers = headers) 
	#获得服务器返回的数据  
	response = urllib2.urlopen(req)
	#处理数据  
	page=response.read()
	BookScore= re.findall(r'<strong class="ll rating_num " property="v:average">(.+?)</strong>', page)[0]
	BookName= re.findall(r'<span property="v:itemreviewed">(.+?)</span>', page)[0].decode()
	BookPic= re.findall(r'<a class="nbg"(.+?)" title', page , re.S)[0].replace('''href="''','').replace(' ','').replace('\n','')
	BookAuthor= re.findall(r'<span class="pl">.*?<a.*?>(.+?)</a>', page, re.S)[0].replace(' ','').replace('\n','').decode()
	BookPublish= re.findall(r'<span class="pl">出版社:</span> (.+?)<br/>', page, re.S)[0].decode()
	BookISBN= re.findall(r'<span class="pl">ISBN:</span> (.+?)<br/>', page, re.S)[0]
	reply= BookName+" "+BookISBN+" "+BookPic+" "+BookAuthor+" "+BookScore+" "+BookPublish+"\n"
	fh.write(reply)
	print "success"

def down(typeNmae):
	for i in range(0,60):
		try:
			links=getBookList(typeNmae,i)
			for url in links:
				try:
					getBookInfo(url)
				except:
					print "error"
		except:
			print "error"

def getBookType():
	url="https://book.douban.com/tag/?view=cloud"
	req=urllib2.Request(url,headers = headers) 
	#获得服务器返回的数据  
	response = urllib2.urlopen(req)
	#处理数据  
	page=response.read()
	typeNmae= re.findall(r'<a href="/tag/(.+?)">', page)
	links=[]
	for i in typeNmae:
		links.append(i.decode())
	return links


class DownloadWorker(Thread):

    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            link = self.queue.get()
            try:
                down(link)
            except HTTPError,e:
                print os.path.basename(link)+': '+e.reason
            except URLError,e:
                print e.__weakref__
            except socket.error,e:
                print e.__weakref__
            self.queue.task_done()

def main():
	try:
############################若出现ip封禁则减少thread数#########################
		threads = 10
############################若出现ip封禁则减少thread数#########################
		links = [l for l in getBookType()]
		queue = Queue()

		for x in range(threads):
		    worker = DownloadWorker(queue)
		    worker.setDaemon(True)
		    worker.start()
		for link in links:
		    queue.put(link)
		queue.join()
	
	except:
		return 'ERROR'


main()
fh.close()