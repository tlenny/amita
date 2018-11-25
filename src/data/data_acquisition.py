# coding=utf-8
#!/usr/bin/python3
'''
Created on 2018年7月10日

@author: ALEX
'''
import urllib.parse
import urllib.request
import time
import zipfile
import os
import data.init_data as init_data

# ****************************config*************************************** #
API_URL = 'https://yucezhe.com/api/v1/data/today'  # url地址
EMAIL = '4461981@qq.com'  # 购买数据时候使用的邮箱地址
API_KEY = 'srxIn4bZqsj3b8UWBKQ4AeN5uHKHtbQO'  # 于页面配置的API KEY
# **************************config_end************************************* #
DATA_DIR = '/opt/tom/data/push-data/'


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    file_path = file_name[:-4]
    if os.path.isdir(file_path):
        pass
    else:
        os.mkdir(file_path)
    for names in zip_file.namelist():
        zip_file.extract(names, file_path)
    zip_file.close()


def save_data(file_name):
    un_zip(file_name)
    file_path = file_name[:-4]
    t = file_path[-10:]
    csv_file_name = file_path + "/" + t+" data.csv"
    print(csv_file_name)
    init_data.init_data(csv_file_name)
    pass


def get_today(product_name, local_file_name):
    """
    :param product_name: the product name, get it from the url of the product homepage
    :param local_file_name: the local file name to save as
    :return: the download url after file saved
    """
    params = {
        'name': product_name,
        'email': EMAIL,
        'key': API_KEY
    }
    params_str = urllib.parse.urlencode(params)
    response = urllib.request.urlopen('%s?%s' % (API_URL, params_str))
    data_download_url = response.read()
    data_download_url = str(data_download_url)
    data_download_url = data_download_url[2:-1]
    print(data_download_url)
    if 'data.yucezhe.com' in data_download_url:
        urllib.request.urlretrieve(data_download_url, local_file_name)
        print('数据已经下载，开始导入')
        save_data(local_file_name)
        return data_download_url
    else:
        return None


def pull_data(product_name):
    """
    this function will auto wait if the data is not ready
    and auto stop when download finished
    :param product_name: equivalent to 'get_today'
    :param local_file_name: equivalent to 'get_today'
    :return: nothing
    """
    
    file_name = time.strftime("%Y-%m-%d", time.localtime())
    local_file_name = DATA_DIR + file_name + '.zip'
    
    _u = get_today(product_name, local_file_name)
    while _u is None:
        print ('[auto run]: data is not ready, retry in 30s')
        time.sleep(600)
        _u = get_today(product_name, local_file_name)


if __name__ == '__main__':
    file_name = time.strftime("%Y-%m-%d", time.localtime())
    file_name = DATA_DIR + file_name + '.zip'
    pull_data('trading-data-push', file_name)
#     un_zip(file_name)
#     save_data(file_name)
