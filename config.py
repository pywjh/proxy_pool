

# 所有网站的解析方式

parse_list = [
    {
        'urls':['http://www.66ip.cn/{}.html'.format(n) for n in range(1,5)],
        'pattern':'//div[@id="main"]/div/div/table//tr[position()>1]',
        'position':{'ip':'./td[1]','port':'./td[2]','address':'./td[3]'},
    },
    {
        'urls':['https://www.kuaidaili.com/free/inha/{}/'.format(n) for n in range(1,10)],
        'pattern':'//div[@id="list"]/table/tbody/tr',
        'position':{'ip':'./td[1]','port':'./td[2]','address':'./td[5]'},
    },
    {
        'urls':['http://www.xicidaili.com/nn/{}'.format(n) for n in range(1,10)],
        'pattern':'//table[@id="ip_list"]/tr[position()>1]',
        'position':{'ip':'./td[2]','port':'./td[3]','address':'./td[4]/a'}
    }
]



DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
