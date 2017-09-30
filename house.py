# -*- coding: utf-8 -*-
"""from lianjia
"""
import sys
import random
import requests
from bs4 import BeautifulSoup

# 指定系统默认编码
reload(sys)
sys.setdefaultencoding('utf8')

HOUSE_DIR = './houses.csv'
MY_FILE = './my.txt'


def write_to_my(s):
    # 带加号为可读写
    #print 'Write to file...',
    hl = open(MY_FILE, 'a')
    hl.write(s)
    hl.close()
    #print 'done',

def calc_my_price(mi, pr):
    return int(10000 * pr / mi)

def get_one_page_house(url):
    print 'Fetching data from ' + url
    r = requests.get(url)
    r.encoding = 'utf8'
    html = r.text
    write_to_my(html)
    soup = BeautifulSoup(html)
    hlst = soup.findAll('div', class_='info clear')
    one_page_house = []
    for h in hlst:
        # house = []
        # area =  h.parent['data-id'][0:4]
        # region = h.find('div',class_='address').string
        region = h.find('div', class_='houseInfo').a.string.strip()
        meters = h.find('div', class_='houseInfo').a.next_sibling.string.strip().replace('|',',')

        if meters.find('别墅'.encode('utf-8')) != -1:
        	continue
            #met = meters.split(',')
            #met.pop(0)
            #meters = ','.join(met)
		
		if region.find('车位'.encode('uft-8')) != -1:
			continue
				
        meters = meters.replace('平米', ' ')
        met = meters.split(',')

        num = meters.count(',')

        if num < 4 :
            metadd = [' 无', ' 无']
            met.extend(metadd)
            meters = ','.join(met)
        elif num < 5:
                met.insert(5, ' 无')
                meters = ','.join(met)

        print met[2]

        price = h.find('div', class_='totalPrice').span.string
        print price

        avg = calc_my_price(float(met[2]), float(price))

        positi = h.find('div', class_='positionInfo').span.next_sibling.string + h.find('div', class_='positionInfo').a.string
        posi = positi.replace('-', ',')
        house = region + meters + "," + price + "," + posi + ',' + str(avg)
        print house
        one_page_house.append(house)
    #print 'done'
    return one_page_house

def write_to_head():
    # 带加号为可读写
    #print 'Write to head...'
    hl = open(HOUSE_DIR, 'a')
    hl.write(('小区,居室,大小,朝向,装修,电梯,价格,楼层,区域,单价\n').encode('GBK'))
    hl.close()
    #print 'done',

def write_to_txt(s):
    # 带加号为可读写
    #print 'Write to file...'
    hl = open(HOUSE_DIR, 'a')
    #newstr = s.encode('utf-8')
    #hl.write(s.encode('utf-8'))
    hl.write(s.encode('GBK'))
    hl.close()
    print 'done',


if __name__ == '__main__':
    url_pre = 'http://xm.lianjia.com/ershoufang/pg'
    #if len(sys.argv) == 3:
    #    page_num = 1
    #    total_page_num = 2
    #else:
    #    print "Please input how many pages to get and the total number of pages"
    #    sys.exit(0)
    # 随机的从总页码中抽取一定数量的页
    page_basket = random.sample(xrange(1, 100), 99)
    i = 0  # 对抓取的页数计数
    write_to_head()
    for p in page_basket:
        url = url_pre + str(p)
        MY_FILE = "./my" + str(p) + ".txt"
        write_to_txt('\n'.join([''.join(h) for h in get_one_page_house(url)]) + '\n')
        i = i + 1
        print '+' + str(i)
