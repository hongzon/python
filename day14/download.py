from time import time
from threading import Thread

import requests

class DownloadHanlder(Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url;
    def run(self):
        filename = self.url[self.url.rfind('/')+1:]
        resp = requests.get(self.url)
        with open('./a.txt','wb') as f:
            f.write(resp.content)

def main():
    # resp = requests.get('http://api.tianapi.com/meinv/?key=APIKey&num=10')
    # data_model = resp.json()
    data_model = ['https://www.baidu.com/s?wd=windows%20%E7%94%9F%E6%88%90ssh%20key&rsv_spt=1&rsv_iqid=0xaeed95ac0003e0cd&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=39042058_7_oem_dg&rsv_enter=1&rsv_sug3=17&rsv_sug1=21&rsv_sug7=100&rsv_t=4dd7lmFNK8bf55gMdb7P15aCBFppViosytTvw%2B3Z5g%2BWUEaLt17dDH%2BR%2BJ0vZxqgdwv6T8cRsB8']
    for mm_dict in data_model:
        url = mm_dict
        # 通过多线程的方式实现图片下载
        DownloadHanlder(url).start()
if __name__ == '__main__':
    main()