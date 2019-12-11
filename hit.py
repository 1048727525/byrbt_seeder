# coding=utf-8

import requests        #导入requests包
import urllib.request
import re
import csv
import login
import VCRmodule
from bs4 import BeautifulSoup
from scrapy import Selector
from lxml import etree
import os



def xpath(i):
    m=i+1
    xpath='//table[@class="torrents"]//tr['+str(m)+']'
    return xpath

def charge(html,xpath):
    charge_path = xpath+'/@class'
    charge = etree.HTML(html).xpath(charge_path)
    charge_information = 0                  ###赋初始值，好习惯
    if len(charge) != 0:
      charge_class = charge[0]
      if charge_class=='free_bg':#免费
         charge_information=1
      elif charge_class=='thirtypercentdown_bg':#30%下载
          charge_information=3
      elif charge_class=='halfdown_bg':#50%下载
          charge_information=4
      elif charge_class=='twouphalfdown_bg':#50%下载&2x上传
          charge_information=5
      elif charge_class=='twoupfree_bg':#2x上传
          charge_information=6
    else:#免费&2x上传
        charge_information = 2
    return charge_information


def name(html,xpath):
    path_name=xpath+'/td[@class="rowfollow"][1]/table/tr/td/a/b/text()'
    name = etree.HTML(html).xpath(path_name)
    print('种子名称：',name[0])
    return name[0]

def intro(html,xpath,cookie):
    path_intro=xpath+'/td[@class="rowfollow"][1]/table/tr/td/a/@href'
    intro = etree.HTML(html).xpath(path_intro)
    introlink='https://bt.byr.cn/'+intro[0]
    print('种子详情页网址',introlink)
    enter = requests.get(introlink, cookies=cookie)
    ent = enter.content
    path_torrent = '//table[@class="mainouter"]/tr[2]/td[@id="outer"]/table[@width="1150"]/tr/td[@class="rowfollow"]/a[@class="index"]/text()'
    #path_torrent= '//table[@class="mainouter"]//tr[1]/td[@id="outer"]/table[@width="1150"]/tr/td[@class="rowfollow"]/a/text()'
    torrent_dl_name=etree.HTML(ent).xpath(path_torrent)
    print('下载torrent名称：',torrent_dl_name[0])
    return torrent_dl_name[0]


def get_downloadlink(html,xpath):
    path_dl = xpath + '/td[@class="rowfollow"][1]/table/tr/td[2]/a/@href'
    dl = etree.HTML(html).xpath(path_dl)
    dllink=dl[0]
    fdllink='https://bt.byr.cn/'+dllink
    return fdllink

def download(torrent_dl_name, url, cookie, name_of_save_torrent):
    path = "./{}/{}".format(name_of_save_torrent, torrent_dl_name) ###format函数增强字符串功能
    #path=str(i)+".exe.torrent"
    #print(response1.cookies)
    download=requests.get(url, cookies=cookie)
    with open(path,"wb") as f:
      f.write(download.content)             #withopen自动close文件

def comments(html,xpath):
    path_comments = xpath + '/td[@class="rowfollow"][2]/b/a/text()'
    comment = etree.HTML(html).xpath(path_comments)
    if comment:
        print('评论数：', comment[0])
        comments_str = str(comment[0])
    else:
        print(0)
        comments_str=0
    return comments_str

def livetime(html,xpath):
    path_livetime = xpath + '/td[@class="rowfollow nowrap"][2]/span/text()'
    livetime = etree.HTML(html).xpath(path_livetime)
    print('存活时间：' ,livetime[0], livetime[1])
    livetime_str=str(livetime[0])+str(livetime[1])
    return livetime_str

def size(response,xpath):
    path_size=xpath+'/td[@class="rowfollow"][3]/text()'
    size = etree.HTML(response).xpath(path_size)
    print('文件大小：',size[0],size[1])
    size_str=str(size[0])+str(size[1])
    return size_str

def seeders(response, xpath):
    path_seeders=xpath+'/td[@class="rowfollow"][4]/b/a/text()'
    seeders=etree.HTML(response).xpath(path_seeders)
    if len(seeders) == 0:
        print('做种数：', 0)
        seeders_str = str(0)
    else:
        print('做种数：',seeders[0])
        seeders_str=str(seeders[0])
    return seeders_str

def leechers(response, xpath):
    path_leechers=xpath+'/td[@class="rowfollow"][5]/b/a/text()'
    leechers=etree.HTML(response).xpath(path_leechers)
    if leechers:
        print('下载数：',leechers[0])
        leechers_str = str(leechers[0])
    else:
        print('下载数：', 0)
        leechers_str= 0
    return leechers_str

def snatched(response, xpath):
    path_snatched=xpath+'/td[@class="rowfollow"][6]/a/b/text()'
    snatched = etree.HTML(response).xpath(path_snatched)
    print('完成数：',snatched[0])
    snatched_str = str(snatched[0])
    return snatched_str

def publisher(response, xpath):
    path_publisher=xpath+'/td[@class="rowfollow"][7]/span/a/b/text()'
    publisher = etree.HTML(response).xpath(path_publisher)
    if publisher:
        print('发布者：', publisher[0])
        publisher_str = str(publisher[0])
    else:
        print('发布者匿名')
        publisher_str = '发布者匿名'
    return publisher_str

def fanye(response):
    path_nextpage='//*[@id="outer"]/table/tbody/tr/td/p[5]/a[6]'

def main(update_seed_num, username, password):
    LEN_OF_GET_TORRENT = update_seed_num
    NAME_OF_SAVE_TORRENT = "torrent_tmp"  ###文件名、下载数这种全局变量放在前面，调整起来方便

    if os.path.exists(NAME_OF_SAVE_TORRENT) == False:
        os.makedirs(NAME_OF_SAVE_TORRENT)  ###创建文件夹

    with open('torrent_information.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        torrentwriter = csv.writer(csvfile, dialect='excel')
        torrentwriter.writerow(
            ['rank'] + ['seed_name'] + ['link'] + ['torrent_name'] + ['price'] + ['reviews'] + ['life'] + ['size'] + [
                'seeders'] + ['downloaders'] + ['finished_num'] + ['updowner'])

        cookie = login.main('https://bt.byr.cn/torrents.php?pktype=1', username, password)
        response = requests.get('https://bt.byr.cn/torrents.php?pktype=1', cookies=cookie)
        res = response.content

        num1 = LEN_OF_GET_TORRENT // 50
        num2 = LEN_OF_GET_TORRENT % 50  ###LEN_OF_GET_TORRENT写明爬取总数目，num1控制翻页 ，num2控制当页下的条数
        for i in range(0, num1 + 1):
            url = 'https://bt.byr.cn/torrents.php?inclbookmarked=0&pktype=1&incldead=0&spstate=0&page=' + str(i)
            ###翻页
            response1 = requests.get(url, cookies=cookie)
            res1 = response1.content
            for j in range(1, 51):
                if i == num1 and j == num2 + 1:
                    break  ###当页下的条数
                k = i * 50 + j
                torrent_xpath = xpath(j)
                torrent_charge = charge(res1, torrent_xpath)
                torrent_name = name(res1, torrent_xpath)
                torrent_name = torrent_name.replace('/', ',')  ###每次命名结束都重新替换
                torrent_url = get_downloadlink(res1, torrent_xpath)
                torrent_dl_name = intro(res1, torrent_xpath, cookie)
                download(torrent_dl_name, torrent_url, cookie, NAME_OF_SAVE_TORRENT)
                torrent_comments = comments(res1, torrent_xpath)
                torrent_livetime = livetime(res1, torrent_xpath)
                torrent_size = size(res1, torrent_xpath).replace(',', '')
                torrent_seeders = seeders(res1, torrent_xpath).replace(',', '')
                torrent_leechers = leechers(res1, torrent_xpath)
                torrent_snatched = snatched(res1, torrent_xpath).replace(',', '')
                torrent_publisher = publisher(res1, torrent_xpath)

                torrentwriter.writerow(
                    [k] + [torrent_name] + [torrent_url] + [torrent_dl_name] + [torrent_charge] + [torrent_comments] + [
                        torrent_livetime] + [torrent_size] + [
                        torrent_seeders] + [torrent_leechers] + [torrent_snatched] + [torrent_publisher])
            if i == num1 and j == num2 + 1:
                break

if __name__ == '__main__':
    main(100, "HYD0525", "HYD112358")