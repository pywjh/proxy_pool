
import time
import requests
from multiprocessing import Process,Queue
import gevent
from gevent import monkey;monkey.patch_all()
from config import parse_list,DEFAULT_HEADERS
from Parser import Parser_response
from Mongo_DB import MongoHelper
from Server import start_server

mongo = MongoHelper()


class Download_HTML(object):

    @staticmethod
    def download(url):
        try:
            print('正在请求{}.....'.format(url))
            r = requests.get(url,headers=DEFAULT_HEADERS)
            r.encoding = 'utf-8'
            if not r.ok:
                raise ConnectionError
            else:
                return r.text
        except Exception as e:
            print('请求失败,异常:',e)


class Proxy_crawl(object):

    proxies_set = set()  # 存放的可用代理

    def __init__(self,queue1):
        self.queue1 = queue1

    def open_spider(self):
        while True:
            proxy_list = mongo.select() # 运行之前  获取数据库中的所有代理
            spawns = []

            for proxy in proxy_list:
                spawns.append(gevent.spawn(decete_from_db,proxy,self.proxies_set))
            gevent.joinall(spawns)

            if len(self.proxies_set) < 5:
                print('当前可用代理数量为{},开始获取代理....'.format(len(self.proxies_set)))
                for parser in parse_list:
                    self.crawl(parser)

            else:
                print('当前可用代理数量大于阀值.....,开始休眠')
                time.sleep(300)


    def crawl(self,parser):
        '''
        对配置文件中的网站进行解析
        :return:
        '''
        Download = Download_HTML()
        for url in parser['urls']:
            time.sleep(2)
            response = Download.download(url)
            if not response:
                return None

            proxy_list = Parser_response.parser_xpath(response,parser)

            for proxy in proxy_list:
                while True:
                    if self.queue1.full():
                        time.sleep(1)
                    else:
                        self.queue1.put(proxy)
                        break

def decete_from_db(proxy,proxies_set):
    proxy = {'ip':proxy[0],'port':proxy[1]}
    result = detect_baidu(proxy)
    if not result:
        mongo.delete(proxy)
        return None
    proxies_set.add('{}:{}'.format(proxy['ip'],proxy['port']))


def detect(queue1,queue2):
    '''
    对queue1中的代理进行检测
    '''

    proxy_list = []
    while True:
        #print('当前队列长度为{}'.format(queue1.qsize()))
        if not queue1.empty():
            proxy = queue1.get()
            proxy_list.append(proxy)

            if len(proxy_list) >=10:
                spawns = []
                for proxy in proxy_list:
                    spawns.append(gevent.spawn(detect_baidu,proxy,queue2))
                gevent.joinall(spawns)
                proxy_list = []

            #detect_baidu(proxy,queue2)




def detect_baidu(proxy,queue2=None):
    proxies = {
        'http':'http://{}:{}'.format(proxy['ip'],proxy['port']),
        'https':'https://{}:{}'.format(proxy['ip'],proxy['port'])
    }
    result = None
    try:
        print(proxies)
        result = requests.get(url='https://www.baidu.com',headers=DEFAULT_HEADERS,proxies=proxies,timeout=5)
    except Exception as e:
        print('代理不可用,以丢弃......')

    if result and queue2:
        print('代理{}可用,添加到可用队列.....'.format(proxy))
        queue2.put(proxy)

    elif result:
        return True





def start_crawl(queue1,):
    P = Proxy_crawl(queue1)
    P.open_spider()



def insert_sql(queue2):
    '''
    不断的读取queue2里面的数据  添加到数据库
    :param queue2:
    :return:
    '''
    while True:
        proxies = queue2.get()
        if proxies:
            mongo.insert(proxies)


if __name__ == '__main__':
    q1 = Queue()  # 所有代理的队列
    q2 = Queue()  # 可用代理的队列
    p1 = Process(target=detect,args=(q1,q2))  # 代理检测
    p2 = Process(target=start_crawl,args=(q1,))  # 下载代理
    p3 = Process(target=insert_sql,args=(q2,))  # 存储
    p4 = Process(target=start_server)            # 接口
    p1.start()
    p2.start()
    p3.start()
    p4.start()


# 微信 ：wangxianlaoshi





