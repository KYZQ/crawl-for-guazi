import xlsxwriter
import requests
import os,re
from lxml import etree
import time
import json
from deal_head import get_cookie
#详细信息
city='全国'
ct='www'
page_num=8358
log_file = open('{}log.txt'.format(city), 'w')
def detail_info(url,head):
    page=requests.get(url,headers=head,timeout=3)
    tree=etree.HTML(page.text)
    temp_dict={}
    #基本信息
    try:
        price=tree.xpath('//span[@class="pricestype"]/text()')[0].strip()
        price=int(float(re.sub('¥','',price))*10000)
        temp_dict['车主报价']=price
        temp_dict['评估师综述']=tree.xpath('//div[@class="test-con"]/text()')[0].strip()
        for item in tree.xpath('//ul[@class="basic-eleven clearfix"]/*'):
            for i in item.xpath('text()'):
                if i.strip()=='':
                        continue
                key=i.strip()
            value=''
            for i in item.xpath('div/text()'):
                if i.strip()=='':
                    continue
                value=i.strip()
            temp_dict[key]=value
        #基本参数 发动机参数 底盘及制动 安全配置 外部配置 内部配置
        temp_dict=part1(tree,temp_dict)
        temp_dict=part2(tree,temp_dict)
    except:
        print('爬取失败：'+page.url )
        log_file.writelines('爬取失败：'+page.url )
        return 0
    return temp_dict

def part1(tree,temp_dict):
    #爬取基本参数 发动机参数 底盘及制动 安全配置 外部配置 内部配置
    for counting in tree.xpath('//th[@colspan="2"]/../..'):
        _=0
        for item in counting.xpath('./*'):
            _+=1
            if _==1:
                #print("正在爬取：{}".format(item.xpath('./*/text()')[0].strip()))
                continue
            try:
                key=item.xpath('./*/text()')[0].strip()
                value=item.xpath('./*/text()')[1].strip()
                if value=='-':
                    value='None'
                    print('{}的值为: -'.format(key))
                temp_dict[key]=value
            except:
                #print('报错，原始数据形式：{},报错的数据没有存进dict！'.format(item.xpath('./*/text()')))
                continue
    return temp_dict
def part2(tree,temp_dict):
    #专业检测
    #print('正在爬取:专业检测')
    for item in tree.xpath('//span[@class="c-name"]'):
        try:
            key=item.xpath('text()')[0].strip()+'('+item.xpath('./following-sibling::*/text()')[0].strip()+')'
            if item.xpath('./following-sibling::*/i/@class')[0]=='icon-right':
                value='合格'
            else:
                value=item.xpath('./following-sibling::*/i/span[2]/text()')[0].strip()
            temp_dict[key]=value
        except:
            #print('报错，原始数据形式：{}{},报错的数据没有存进dict！'.format(item.xpath('text()'),item.xpath('./following-sibling::*/text()')))
            continue
    #外观内饰检测
    for item in tree.xpath('//li[@class="exterior"]/*'):
        if item.tag=='div':
            key=item.xpath('./text()')[0].strip()
            if item.xpath('./span/i/@class')[0].strip()=='icon-right':
                value='合格'
            else:
                value=item.xpath('./span/i/span[2]/text()')[0].strip()
        else:
            #外观内饰检测 38项
            key=item.text
            value=item.xpath('./span/text()')[0].strip()
        temp_dict[key]=value
    return temp_dict
#处理一级网页
def deal_page(url,head):
    page=requests.get(url,headers=head,timeout=3)
    tree=etree.HTML(page.text)
    page_cars_data=[]
    i=0
    base_url='https://www.guazi.com'
    for item in tree.xpath('//ul[@class="carlist clearfix js-top"]/*[name()="li"]'):
        i+=1
        print('爬取当前页面第{}辆车'.format(i))
        time.sleep(0.2)
        car_url=base_url+item.xpath('./a/@href')[0]
        car_infor=detail_info(car_url,head)
        if car_infor!=0:
            page_cars_data.append(car_infor)
    return page_cars_data
#爬取
def crawl(page_num,head):
    data=[]
    try:
        for i in range(1,page_num+1):
            print('爬取第{}页'.format(i))
            url = 'https://www.guazi.com/{}/buy/o{}/#bread'.format(ct,i)
            try:
                page_car_data=deal_page(url, head)
            except:
                log_file.writelines('page_car 失败:'+url)
                continue
            data.extend(page_car_data)
    except:
        with open("{}({}).json".format(city,len(data)), "w") as file:
            print('爬去完毕，汽车数量：',len(data))
            json.dump(data, file)
    with open("{}({}).json".format(city,len(data)), "w") as file:
        print('爬去完毕，汽车数量：', len(data))
        json.dump(data, file)
#for linux
# head={
#   'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/10.04 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2'
# }
#for windows:
#
head={'User-Agent':'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'}

#
url='https://www.guazi.com/{}/buy/o1/#bread'.format(ct)
head=get_cookie(url,head)
crawl(page_num,head)
log_file.close()