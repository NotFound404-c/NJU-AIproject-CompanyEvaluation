import pandas as pd
from tqdm import tqdm
import warnings
import sys
from company_zhengzehua import gentwoname
from company_spider import companyspider
from company_spider2 import companyspider2
from company_breakpoint import company_breakpoint, delete
from company_spider3 import companyspiderr

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8-sig', buffering=1)
warnings.filterwarnings("ignore")

file_path = '/Users/vitol/PycharmProjects/pythonProject/职q爬虫/源文件/company_url.csv'
file_path1 = '/Users/vitol/PycharmProjects/pythonProject/职q爬虫/源文件/companiesinit.csv'
file_path2 = '/Users/vitol/PycharmProjects/pythonProject/职q爬虫/源文件/TRD_Co.csv'

df_try = pd.read_csv(file_path1)
df_try2 = pd.read_csv(file_path)
cookies_dict = {
    ' _uab_collina=173536355223355066320828; 1420ba6bb40c9512e9642a1f8c243891=bf9f31db-e0d5-45da-bc60-4fb50c193ad3; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221194158044%22%2C%22first_id%22%3A%221940b9f7a492144-04d636145e1ccbc-49193d01-1892970-1940b9f7a4a1f2a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0MGI5ZjdhNDkyMTQ0LTA0ZDYzNjE0NWUxY2NiYy00OTE5M2QwMS0xODkyOTcwLTE5NDBiOWY3YTRhMWYyYSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjExOTQxNTgwNDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221194158044%22%7D%2C%22%24device_id%22%3A%221940b9f7a492144-04d636145e1ccbc-49193d01-1892970-1940b9f7a4a1f2a%22%7D; Hm_lpvt_d26c088bb03e43df2051e9eecc560781=1735372037; Hm_lvt_d26c088bb03e43df2051e9eecc560781=1735361793; at=b650e8d195dd4013aa39e6dea73f6eaf; rt=9216acec3222475cb0b6453821b55e0b; zp_passport_deepknow_sessionId=2a3d74d2s0ae674f108288b01d8023f77bcc; _uab_collina=173536829927109813514721; searchHistory=%5B%22%u5E73%u5B89%u94F6%u884C%22%5D; HMACCOUNT=A297F036178D3ACD; sajssdk_2015_cross_new_user=1; x-zp-client-id=57a8da9e-acd8-4738-a455-9cca9f378f17': 'https://zq.zhaopin.com/discover-site/moment/0_1_0/getMomentListByCompanyOrgNumber?orderStr={}0&orgNumber={}&at=b650e8d195dd4013aa39e6dea73f6eaf&rt=9216acec3222475cb0b6453821b55e0b&x-zp-client-id=57a8da9e-acd8-4738-a455-9cca9f378f17'
}
cookie_pool = [
    ' _uab_collina=173536355223355066320828; 1420ba6bb40c9512e9642a1f8c243891=bf9f31db-e0d5-45da-bc60-4fb50c193ad3; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221194158044%22%2C%22first_id%22%3A%221940b9f7a492144-04d636145e1ccbc-49193d01-1892970-1940b9f7a4a1f2a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0MGI5ZjdhNDkyMTQ0LTA0ZDYzNjE0NWUxY2NiYy00OTE5M2QwMS0xODkyOTcwLTE5NDBiOWY3YTRhMWYyYSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjExOTQxNTgwNDQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221194158044%22%7D%2C%22%24device_id%22%3A%221940b9f7a492144-04d636145e1ccbc-49193d01-1892970-1940b9f7a4a1f2a%22%7D; Hm_lpvt_d26c088bb03e43df2051e9eecc560781=1735372037; Hm_lvt_d26c088bb03e43df2051e9eecc560781=1735361793; at=b650e8d195dd4013aa39e6dea73f6eaf; rt=9216acec3222475cb0b6453821b55e0b; zp_passport_deepknow_sessionId=2a3d74d2s0ae674f108288b01d8023f77bcc; _uab_collina=173536829927109813514721; searchHistory=%5B%22%u5E73%u5B89%u94F6%u884C%22%5D; HMACCOUNT=A297F036178D3ACD; sajssdk_2015_cross_new_user=1; x-zp-client-id=57a8da9e-acd8-4738-a455-9cca9f378f17'
]
company_infomat = pd.read_csv(file_path2)
while not company_infomat['Stkcd'].empty:
    try:
        company_info = gentwoname(company_infomat)
        company_list = company_info['ShortName'].tolist()
        company_list_short = company_info['NickName'].tolist()
        for a in tqdm(range(0, len(company_list))):
            df_try3 = pd.read_csv(file_path)
            idlist, df_try3 = companyspider(cookie_pool, a, company_list, company_list_short, df_try3)
            df_try2 = pd.concat([df_try2, df_try3], axis=0)
            for company_id in idlist:
                df_try4 = pd.read_csv(file_path1)
                df_try4 = companyspider2(cookies_dict, cookie_pool, company_id, df_try4, company_list, a)
                df_try = pd.concat([df_try, df_try4], axis=0)
            company_infomat = delete(company_infomat)
            company_infomat = company_infomat.reset_index(drop=True)
        df_try.to_csv(file_path1, mode='a', index=False, encoding='utf-8-sig',
                      sep=',', header=False)
        df_try2.to_csv(file_path, mode='a', index=False, encoding='utf-8-sig',
                       sep=',', header=False)
    except Exception as e:
        print(e)
        df_try = company_breakpoint(df_try, company_list[a])
        df_try2 = company_breakpoint(df_try2, company_list[a])
        continue

