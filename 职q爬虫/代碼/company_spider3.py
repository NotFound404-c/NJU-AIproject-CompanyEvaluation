import json
import time
import numpy as np
import pandas as pd
from lxml import etree
from curl_cffi import requests
from urllib3.util.retry import Retry
# from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter


def companyspiderr(cookie, n, list1, short_list, dft):
    dictt = {}
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # 设置重试次数
        status_forcelist=[302, 303, 429, 500, 502, 503, 504, 400],  # 设置要重试的HTTP状态码
        backoff_factor=1  # 设置退避因子，用于控制重试之间的延迟时间
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    # session.mount("https://", adapter)
    # session.mount("http://", adapter)
    # user_random = UserAgent().random
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
        'Cookie': np.random.choice(cookie)
    }
    i = 0
    while True:
        target_url = f"https://zq.zhaopin.com/gongsidianping/0-0-{short_list[n]}-{i}"
        response = session.get(target_url, headers=headers)
        xmlContent = etree.HTML(response.text)
        # 发现一个指定位置的script标签，里面有需要爬取的部分url数据，将其提取出来
        text_target = xmlContent.xpath('//body/script[1]')
        texts1 = ''.join([p.xpath('string(.)') for p in text_target])
        # 将字符串形式的文本转化为json格式f
        try:
            json_form = texts1.replace('__INITIAL_STATE__=', '')
            wenben = json.loads(json_form)
        except:
            time.sleep(10)
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
                    'Cookie': np.random.choice(cookie)
                }
                target_url = f"https://zq.zhaopin.com/gongsidianping/0-0-{short_list[n]}-{i}"
                response = session.get(target_url, headers=headers)
                xmlContent = etree.HTML(response.text)
                text_target = xmlContent.xpath('//body/script[1]')
                texts1 = ''.join([p.xpath('string(.)') for p in text_target])
                json_form = texts1.replace('__INITIAL_STATE__=', '')
                wenben = json.loads(json_form)
            except:
                print(f"json error{n}")
                dictt['companyid'] = list1[n]
                dictt['url'] = None
                dictt['name'] = None
                dictt['orgNumber'] = None
                df1 = pd.DataFrame.from_records([dictt])
                dft = pd.concat([dft, df1], axis=0)
                break
        companies_data = wenben['companies']
        companies_info = [(i['name'], i['orgNumber']) for i in companies_data]
        if i == 0 and companies_info == []:
            dictt['companyid'] = list1[n]
            dictt['url'] = None
            dictt['name'] = None
            dictt['orgNumber'] = None
            df1 = pd.DataFrame.from_records([dictt])
            dft = pd.concat([dft, df1], axis=0)
            print("No data")
            break
        # 如果获取到空集，则代表没这一页，则break退出循环
        if not companies_info:
            break
        companies_df = pd.DataFrame(companies_info, columns=['name', 'orgNumber'])
        # 整合成url形式
        companies_df['url'] = companies_df['orgNumber'].apply(
            lambda x: 'https://zq.zhaopin.com/companyDetail/' + str(x) + '/')
        i += 10
        companies_df.insert(0, 'companyid', list1[n])
        dft = pd.concat([dft, companies_df], axis=0)
    company_id_list = dft['orgNumber'].tolist()
    return company_id_list, dft