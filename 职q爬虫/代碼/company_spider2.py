import time
from urllib3.util.retry import Retry
import numpy as np
import pandas as pd
from curl_cffi import requests
# from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter


def companyspider2(cookiedict, cookie, id, dff, list2, n):
    if id == None:
        return dff
    else:
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
        page = 0
        total_comments = 0
        company_dict = {}
        while True:
            comment_url = cookiedict[headers['Cookie']].format(page, id)
            res = session.get(comment_url, headers=headers, verify=False)
            try:
                recordjs = res.json()
            except:
                try:
                    print(f"json error{n}")
                    time.sleep(10)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
                        'Cookie': np.random.choice(cookie)
                    }
                    comment_url = cookiedict[headers['Cookie']].format(page, id)
                    res = session.get(comment_url, headers=headers, verify=False)
                    recordjs = res.json()
                except:
                    break
            try:
                if not recordjs['data']['moments']:
                    break
            except KeyError:
                try:
                    print("KeyError")
                    time.sleep(10)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
                        'Cookie': np.random.choice(cookie)
                    }
                    comment_url = cookiedict[headers['Cookie']].format(page, id)
                    res = session.get(comment_url, headers=headers, verify=False)
                    recordjs = res.json()
                    if not recordjs['data']['moments']:
                        break
                except:
                    break
            if page == 0:
                company_info = recordjs['data']['moments'][0]['company']
                criterion_info = company_info['criterionPercentages']
                company_dict.update({k: v for k, v in company_info.items() if
                                     k in ['name', 'orgNumber', 'createdTime', 'reviewNum', 'totalScore',
                                           'likeCompanyClang', 'likeSalary', 'likeWorking']})
                company_dict.update(criterion_info)
                company_dict['FirstTime'] = company_dict.pop('createdTime', None)
                company_dict['companyTotalScore'] = company_dict.pop('totalScore', None)
                company_dict['totalLikeCC'] = company_dict.pop('likeCompanyClang', None)
                company_dict['totalLikeS'] = company_dict.pop('likeSalary', None)
                company_dict['totalLikeW'] = company_dict.pop('likeWorking', None)
                company_dict['FirstTimeminutes'] = company_dict['FirstTime'].split(' ')[1]
                company_dict['FirstTimeminutes'] = company_dict['FirstTimeminutes'].split('.')[0]
                company_dict['FirstTime'] = company_dict['FirstTime'].split(' ')[0]

            comment_num = len(recordjs['data']['moments'])
            total_comments = total_comments + comment_num
            for z in range(comment_num):
                # 读取每条comment记录
                comment_item = recordjs['data']['moments'][z]
                content = comment_item['companyStarScore']
                comment_dict = {k: v for k, v in content.items() if
                                k in ['labelNameList', 'positiveContent', 'negativeContent', 'totalScore',
                                      'likeCompanyClang', 'likeSalary', 'likeWorking']}
                comment_dict.update(
                    {k: v for k, v in comment_item.items() if k in ['createdTime', 'readNum', 'readNumShow']})

                total_dict = {**company_dict, **comment_dict}
                total_dict['createdminutes'] = total_dict['createdTime'].split(' ')[1]
                total_dict['createdminutes'] = total_dict['createdminutes'].split('.')[0]
                total_dict['createdTime'] = total_dict['createdTime'].split(' ')[0]
                total_dict['companyid'] = list2[n]
                df2 = pd.DataFrame.from_records([total_dict])
                dff = pd.concat([dff, df2], axis=0)
            page += 1
        return dff
