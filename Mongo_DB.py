import pymongo


class MongoHelper(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['tanzhou_homework']
        self.proxy = self.db['proxy']


    def insert(self,data=None):
        if data:
            self.proxy.save(data)


    def delete(self,data=None):
        if data:
            self.proxy.remove(data)


    def update(self,data,conditions):
        if conditions and data:
            self.proxy.update(data,{'$set':conditions})


    def select(self,data=None):
        if data:
            items = self.proxy.find(data)

        else:
            data = {}
            items = self.proxy.find(data)

            results = []
            for item in items:
                result = (item['ip'],item['port'],item['address'])

                results.append(result)

            return results



if __name__ == '__main__':
    mongo = MongoHelper()
    #mongo.insert({'ip': '218.204.129.195', 'port': '43809', 'address': '江西省南昌市  移动'})
    print(mongo.select())


