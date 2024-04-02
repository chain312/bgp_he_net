#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File       ：flag_map.py
@IDE        ：PyCharm
@Author     ：chain312
@Date       ：2023/8/30 14:15
@Description：
'''

from bs4 import BeautifulSoup
import requests
import random
from common.sql_operate import Sql_operate
import re
from tqdm import tqdm
import yaml

conn = None
cursor = None
USERAGENTS = [ua.strip() for ua in open("config/user_agent").readlines()]
proxy = None
queue_as=None
def read_config():
    yaml_file = "config/config.yaml"

    with open(yaml_file, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg
def get_proxy():
    cfg=read_config()
    return requests.get(cfg["proxy"]["config"]["url"]+"get?type=https").json()

def delete_proxy(proxy):
    cfg = read_config()
    requests.get(cfg["proxy"]["config"]["url"]+"delete/?proxy={}".format(proxy))


def connect_database():
    cfg = read_config()
    global conn, cursor
    print(cfg)
    conn, cursor = Sql_operate(cfg["mysql"]["config"]["host"], int(cfg["mysql"]["config"]["port"]), cfg["mysql"]["config"]["user"], cfg["mysql"]["config"]["password"],'').connect_sql()
def close_database():
    global conn, cursor
    if cursor:
        cursor.close()
    if conn:
        conn.close()
def get_html(url):
    max_retries = 100
    global  proxy
    for retry in range(max_retries):
        try:
            base_url = "https://bgp.he.net/"
            req_url = base_url+url
            burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0",
                             "User-Agent": USERAGENTS[random.randint(0,len(USERAGENTS)-1)],
                             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                             "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                             "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                             "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6"}

            # res = requests.get('https://myip.ipip.net', timeout=5,proxies={"https": "http://{}".format(proxy)}).text
            # print(res)
            respone=requests.get(req_url, headers=burp0_headers,timeout=60,proxies={"https": "http://{}".format(proxy)})
            if respone.status_code==200:
                print('*'*100)
                if 'have reached your query limit on' in respone.text:
                    proxy = get_proxy().get("proxy")
                    print(proxy)
                    delete_proxy(proxy)
                else:
                    return respone
            else:
                print('爬取错误')
                print(base_url)
        except Exception as  e:
            proxy = get_proxy().get("proxy")
            print("proxy")
            print(proxy)
            delete_proxy(proxy)
            print(e.__str__())

def as_get_overview(as_name):
    respone = get_html(as_name)
    print('as_name')
    try:
        Prefixes_Originated_all_reg = re.compile('Prefixes Originated \(all\): (\S+)\<')
        Prefixes_Originated_all = Prefixes_Originated_all_reg.findall(respone.text)
        Prefixes_Originated_v4_reg = re.compile('Prefixes Originated \(v4\): (\S+)\<')
        Prefixes_Originated_v4 = Prefixes_Originated_v4_reg.findall(respone.text)
        Prefixes_Originated_v6_reg = re.compile('Prefixes Originated \(v6\): (\S+)\<')
        Prefixes_Originated_v6 = Prefixes_Originated_v6_reg.findall(respone.text)
        Prefixes_Announced_all_reg = re.compile('Prefixes Announced \(all\): (\S+)\<')
        Prefixes_Announced_all = Prefixes_Announced_all_reg.findall(respone.text)
        Prefixes_Announced_v4_reg = re.compile('Prefixes Announced \(v4\): (\S+)\<')
        Prefixes_Announced_v4 = Prefixes_Announced_v4_reg.findall(respone.text)
        Prefixes_Announced_v6_reg = re.compile('Prefixes Announced \(v6\): (\S+)\<')
        Prefixes_Announced_v6 = Prefixes_Announced_v6_reg.findall(respone.text)

        condition = [Prefixes_Originated_all[0],Prefixes_Originated_v4[0],Prefixes_Originated_v6[0],Prefixes_Announced_all[0],Prefixes_Announced_v4[0],Prefixes_Announced_v6[0]]
    except Exception as e:
        print(as_name)
        print(respone.text)
        print(Prefixes_Originated_all,Prefixes_Originated_v4,Prefixes_Originated_v6,Prefixes_Announced_all,Prefixes_Announced_v4,Prefixes_Announced_v6)
        return 0

    condition[0] = condition[0].replace(',', '') if ',' in condition[0] else int(condition[0])
    condition[1] = condition[1].replace(',', '') if ',' in condition[1] else int(condition[1])
    condition[2] = condition[2].replace(',', '') if ',' in condition[2] else int(condition[2])
    condition[3] = condition[3].replace(',', '') if ',' in condition[3] else int(condition[3])
    condition[4] = condition[4].replace(',', '') if ',' in condition[4] else int(condition[4])
    condition[5] = condition[5].replace(',', '') if ',' in condition[5] else int(condition[5])
    condition.append(as_name)
    try:
        if not conn.open:
            connect_database()
        cursor.execute(
            "insert into as_info(Prefixes_Originated_all,Prefixes_Originated_v4,Prefixes_Originated_v6,Prefixes_Announced_all,Prefixes_Announced_v4,Prefixes_Announced_v6,ASN)value(%s,%s,%s,%s,%s,%s,%s)",
            tuple(condition))
        conn.commit()
    except Exception as e:
        print(e.__str__())
        print(as_name)
    soup = BeautifulSoup(respone.text.encode('utf-8'), "lxml")
    html_tbody = soup.find_all('tbody')
    reg_v4 = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    reg_v6 = re.compile('\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*')
    reg_country = re.compile('/images/flags/(\S+).gif')
    for tbody in html_tbody:

        html_tr = tbody.find_all('tr')
        for tag in tqdm(html_tr, desc="读取" + as_name + 'AS'):
            td_tags = tag.find_all('td')
            ip_v4 = reg_v4.findall(str(td_tags))
            ip_v6 = reg_v6.findall(str(td_tags))
            if len(ip_v4)>0 or len(ip_v6)>0:
                if len(td_tags) == 2:
                    as_details_condition = []
                    as_details_condition.append(as_name)
                    for td in td_tags:
                        td_text = td.get_text().replace('\t', '').replace('\n', '')
                        as_details_condition.append(td_text)
                    ip_type = reg_v4.findall(as_details_condition[1])
                    country = reg_country.findall(str(tag))
                    if len(country) >0:
                        cn = 'cn' if country[0] in ['hk', 'tw', 'mo'] else country[0]
                        as_details_condition.append(cn)
                    else:
                        as_details_condition.append('')
                    if len(ip_type)>0:
                        as_details_condition.append(0)
                    else:
                        as_details_condition.append(1)
                    try:
                        if not conn.open:
                            connect_database()
                        cursor.execute(
                            "insert into as_details(ASN,Prefix,Description,flag,type)value(%s,%s,%s,%s,%s)",
                            tuple(as_details_condition))

                        conn.commit()
                    except Exception as e:
                        print(e.__str__())
                        print(as_details_condition)
                else:
                    # print('len(td_tags) == 2')
                    if 'exchange' not in str(td_tags):
                        print('len(td_tags) == 2')
                        print(td_tags)
                        print(tbody)
                        print(as_name)
            else:
                # print("len(ip_v4)>0 or len(ip_v6)>0")
                # print(td_tags)
                break
def country_get_as(country):
    respone = get_html('country/'+country)
    soup = BeautifulSoup(respone.text.encode('utf-8'), "lxml")
    html_tr = soup.tbody.find_all('tr')

    for tag in tqdm(html_tr, desc="读取"+country+'AS'):
        td_tags = tag.find_all('td')
        if len(td_tags) == 6:
            condition = []
            for td in td_tags:
                td_text = td.get_text().replace('\t', '').replace('\n', '')
                condition.append(td_text)
            condition[2] = condition[2].replace(',', '') if ',' in condition[2] else int(condition[2])
            condition[3] = condition[3].replace(',', '') if ',' in condition[3] else int(condition[3])
            condition[4] = condition[4].replace(',', '') if ',' in condition[4] else int(condition[4])
            condition[5] = condition[5].replace(',', '') if ',' in condition[5] else int(condition[5])
            if  not conn.open:
                connect_database()
            cursor.execute("insert into country(ASN,Name,Adjacencies_v4,Routes_v4,Adjacencies_v6,Routes_v6)value(%s,%s,%s,%s,%s,%s)", tuple(condition))
            conn.commit()
            # queue_as.put(condition[0])
            # close_database()
            as_get_overview(condition[0])
        else:
            print(td_tags)
def report_world():
    respone=get_html('report/world')
    soup = BeautifulSoup(respone.text.encode('utf-8'), "lxml")
    try:
        html_tr=soup.tbody.find_all('tr')
    except:
        return 0
    for tag in tqdm(html_tr, desc="读取总进度"):
        td_tags=tag.find_all('td')
        if len(td_tags)==4:
            condition=[]
            for td in td_tags[0:3]:
                td_text = td.get_text().replace('\t', '').replace('\n', '')
                condition.append(td_text)
                # print(td_text)
            condition[2]= condition[2].replace(',','') if ',' in condition[2] else int(condition[2])
            CC1 = 'CN' if condition[1] in ['HK','TW','MO'] else condition[1]
            condition.append(CC1)
            if  not conn.open:
                connect_database()
            try:
                cursor.execute("insert into report_world(Description, CC, ASNs,CC1)value(%s,%s,%s,%s)", tuple(condition))
                conn.commit()
                # close_database()
            except Exception as  e:
                print("存储report/world失败")
                print(e.__str__())
                print(condition)
            country_get_as(condition[1])
        else:
            print(td_tags)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    connect_database()
    report_world()
    close_database()

