# -*- coding:utf-8 -*-
from requests import post, get, exceptions
import time

try:
    from androidhelper import Android
except Exception as e:
    print('no module named androidhelper')
from os.path import exists, join
from os import mkdir, remove, listdir


'''
Version: 1.2.0
UpdateTime: March 31th, 2018
UpdateContent: 1, Old site has changed it's domain name;
               2, Fix error cannot remove files correctly;
               3, Change to Python3.
'''
# Decode QRcode to SSurl
def qr2str(pic_name):
    # this is a online website server which could decode QRcode
    upload_url = 'http://jiema.wwei.cn/fileupload.html?op=jiema&token=4fdaa2d1c06883389da0cd96dd0cf3852a0700a2'
    files = {'file': open(join('../SSRSet/', pic_name), 'rb')}
    # 'r' is a response for post
    r = post(upload_url, files=files).text
    # print(r)
    if not r == '':
        # print(r)
        ss = eval(r)['data'].replace('\\', '')
        print(ss + '\n')
        with open(join('../SSRSet/', time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.txt'), 'a+') as file:
            file.write(pic_name.split('.')[0] + '\t' + ss + '\n')
        # copy a ssurl to clipboard
        if pic_name == 'us01.png':
            try:
                droid = Android()
                droid.setClipboard(ss)
            except Exception as e:
                print('not in a android env')
            # droid.setClipboard('clippersth')
            # print droid.getClipboard()
            # 或者直接 print droid().getClipboard()
            # 设置剪贴板内容是setClipboard


# Download QRcode from target url
def down_qr(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": '1',
        "Host": "my.freess.org",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": '1',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    pic_name = url.split('/')[5]
    try:
        print('Trying to get target QRcode' + pic_name) 
        result = get(url, headers=headers)  # , timeout=10
    except Exception as e:
        print('Failed to get target QRcode ' + e) 
    with open(join('../SSRSet/', pic_name), 'wb') as file:
        file.write(result.content)
        print(pic_name + ' has been saved') 
    return pic_name


def main():
    if exists('../SSRSet'):
        for i in listdir('../SSRSet'):
            try:
                remove(join('../SSRSet',i))
            except Exception as e:
                print(e)
        # mkdir('../SSRSet')
    else:
        mkdir('../SSRSet')
    ss_url = ['https://my.freess.org/images/servers/jp01.png',
              'https://my.freess.org/images/servers/jp02.png',
              'https://my.freess.org/images/servers/jp03.png',
              'https://my.freess.org/images/servers/us01.png',
              'https://my.freess.org/images/servers/us02.png',
              'https://my.freess.org/images/servers/us03.png']
    for url in ss_url:
        qr2str(down_qr(url))
        # down_qr(url)


main()
