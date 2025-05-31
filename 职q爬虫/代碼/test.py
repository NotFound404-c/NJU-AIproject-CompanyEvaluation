from curl_cffi import requests

import json
import time
import numpy as np
import pandas as pd
from lxml import etree

from urllib3.util.retry import Retry
# from fake_user_agent import UserAgent
from requests.adapters import HTTPAdapter
from company_spider3 import companyspiderr

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
        'Cookie': ' _uab_collina=173536355223355066320828; 1420ba6bb40c9512e9642a1f8c243891=bf9f31db-e0d5-45da-bc60-4fb50c193ad3; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221194158044%22%2C%22first_id%22%3A%221940b9f7a492144-04d636145e1ccbc-49193d01-1892970-1940b9f7a4a1f2a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0MGI5ZjdhNDkyMTQ0LTA0ZDYzNjE0NWUxY2NiYy00OTE5M2QwMS0xODkyOTcwLTE5NDBiOWY3YTRhMWYyYSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjExOTQxNTgwNDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221194158044%22%7D%2C%22%24device_id%22%3A%221940b9f7a492144-04d636145e1ccbc-49193d01-1892970-1940b9f7a4a1f2a%22%7D; Hm_lpvt_d26c088bb03e43df2051e9eecc560781=1735372037; Hm_lvt_d26c088bb03e43df2051e9eecc560781=1735361793; at=b650e8d195dd4013aa39e6dea73f6eaf; rt=9216acec3222475cb0b6453821b55e0b; zp_passport_deepknow_sessionId=2a3d74d2s0ae674f108288b01d8023f77bcc; _uab_collina=173536829927109813514721; searchHistory=%5B%22%u5E73%u5B89%u94F6%u884C%22%5D; HMACCOUNT=A297F036178D3ACD; sajssdk_2015_cross_new_user=1; x-zp-client-id=57a8da9e-acd8-4738-a455-9cca9f378f17'
    }

response = requests.get(
    'https://zq.zhaopin.com/gongsidianping/0-0-平安银行/',

    headers=headers,
)
xmlContent = etree.HTML(response.text)
# 发现一个指定位置的script标签，里面有需要爬取的部分url数据，将其提取出来
text_target = xmlContent.xpath('//body/script[1]')
texts1 = ''.join([p.xpath('string(.)') for p in text_target])
json_form = texts1.replace('__INITIAL_STATE__=', '')
wenben = json.loads(json_form)
companies_data = wenben['companies']
companies_info = [(i['name'], i['orgNumber']) for i in companies_data]
print(companies_info)