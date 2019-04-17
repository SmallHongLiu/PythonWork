from requests_html import HTMLSession

# session = HTMLSession()
# r = session.get('https://search.jd.com/Search?keyword=x1&enc=utf-8&wq=x1&pvid=add52cb63f7e4887b5ba29406a5756ba')
# link_list = r.html.absolute_links
# print(link_list)

'''使用requests-html'''
session = HTMLSession()

r = session.get('http://plugins.svn.wordpress.org/')

print(r)
print(r.url)

links = r.html.absolute_links

print(links)

slugs = [link.replace('/', '') for link in links]

plugins_urls = ["https://api.wordpress.org/plugins/info/1.0/{}.json".format(slug) for slug in slugs]

with open('all_plugins_urls.txt', 'a') as out:
    out.write('\n'.join(plugins_urls))

'''使用BeautifulSoup
import requests
from bs4 import BeautifulSoup

html = requests.get("http://plugins.svn.wordpress.org/").text

soup = BeautifulSoup(html, features='lxml')
lis = soup.find_all('li')
base_url = "https://api.wordpress.org/plugins/info/1.0/"

with open('all_plugins_urls.txt','a') as out:
    for a in soup.find_all('a', href=True):
        out.write(base_url + a['href'].replace('/', '') + ".json" + "\n")

'''

import scrapy
