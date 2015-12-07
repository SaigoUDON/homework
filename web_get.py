# -*- coding: utf-8 -*-
# from html.parser import HTMLParser
# from urllib.request import urlopen
# class MyHTMLParser(HTMLParser):
#      def handle_starttag(self, tag, attrs):
#         if tag == 'a':
#              print(dict(attrs).get('href'))

# f = urlopen('http://qiita.com/advent-calendar/2014')
# parser = MyHTMLParser()
# parser.feed(f.read().decode('utf-8'))

# import lxml.html
# root = lxml.html.parse('http://qiita.com/advent-calendar/2014').getroot()
# root.cssselect('title')[0]
# # <Element title at 0x10b391c78>
# root.cssselect('title')[0].text
# # '2014年のAdvent Calendar一覧 - Qiita'
# for a in root.xpath('//a'):
# 	print(a.get('href'))

# from pyquery import PyQuery as pq
# d = pq(url='http://qiita.com/advent-calendar/2014')
# d('title')
# # [<title>]
# d('title').text()
# '2014年のAdvent Calendar一覧 - Qiita'
# for a in d('a').items():
# 	print(a.attr('href'))

# from urllib.request import urlopen
# f = urlopen('http://qiita.com/advent-calendar/2014')
# f.code
import requests
r = requests.get('http://item.rakuten.co.jp/marutyu-sake/2012-4296/')
# print r.status_code
# print r.headers['content-type']
# print r.encoding
print r.text.encode('utf-8')