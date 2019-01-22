
from lxml import etree

class Parser_response(object):


    @staticmethod
    def parser_xpath(response,parser):
        '''
        根据parser里面的规则 对response进行解析
        :param response:
        :param parser:
        :return:
        '''
        etre = etree.HTML(response)

        items = etre.xpath(parser['pattern'])

        proxy_list = []
        for item in items:
            try:
                ip = item.xpath(parser['position']['ip'])[0].text
                port = item.xpath(parser['position']['port'])[0].text
                address = item.xpath(parser['position']['address'])[0].text
            except Exception as e:
                continue
            else:
                proxy = {'ip':ip,'port':port,'address':address}
                proxy_list.append(proxy)


        return proxy_list
            #print('ip地址:',ip)






    def parser_re(self):
        pass