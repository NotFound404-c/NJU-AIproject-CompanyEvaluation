import re


# 對公司名稱做正則化處理
def GenShortName(name):
    if '(' in name:
        name = name.split('(')[0]
    if '集团' in name:
        name = name.split('集团')[0]
    if '股份' in name:
        name = name.split('股份')[0]
    if '控股' in name:
        name = name.split('控股')[0]
    name = name.replace("市", "")
    return name


def GenNickName(name):
    new_name = re.sub(r'[^\u4e00-\u9fa5]+', '', name)
    return new_name


def gentwoname(company_dataframe):
    company_information = company_dataframe[['Stkcd', 'Stknme', 'Conme']]
    company_information['ShortName'] = company_information['Conme'].apply(lambda x: GenShortName(x))
    company_information['NickName'] = company_information['Stknme'].apply(lambda x: GenNickName(x))
    return company_information
