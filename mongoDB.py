# mongodb://m-i-mirage:nKTwCt4R8u5dG4AIhCwN2IPxJ8WdiZ1cQJVUeJgaVzEenYApPZzrRrciWSaXwTkqCjancvIl01yeACDbLnA6yA%3D%3D@m-i-mirage.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@m-i-mirage@
import pymongo
class mongoDBconnect():
    def __init__(self) -> None:
        myclient = pymongo.MongoClient('mongodb://m-i-mirage:nKTwCt4R8u5dG4AIhCwN2IPxJ8WdiZ1cQJVUeJgaVzEenYApPZzrRrciWSaXwTkqCjancvIl01yeACDbLnA6yA%3D%3D@m-i-mirage.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@m-i-mirage@')
        self.connect = myclient['sleepTimeDB'].chatbotData
        print('MongoDB connected')
        
    def readAlgorithm(self,algorithmName,query):
        try:
            tests = self.connect.find({"name":"algorithm"})
            if tests is None:
                return 'Sorry nothing found. Maybe you can try /GptON.'
            result = [result[algorithmName][query] for result in tests][0]
            return result
        except (IndexError, ValueError):
            print(IndexError)
            print(ValueError)
            return 'Sorry, there are some errors in MongoDB.'
        
    def increaseLog(self,name,id):
        try:
            tests = self.connect.find_one({"name":id+"language"})
            if tests is None:
                # return 'Sorry nothing found. Maybe you can try /GptON.'
                newID = {
                    "name":id+"language",
                    "javascript":0,
                    "python":0,
                    "java":0,
                    "c":0,
                    "c++":0,
                    "c#":0,
                    "css":0,
                    "html":0
                }
                self.connect.insert_one(newID)
                return self.increaseLog(name,id)
            # result = [result[name] for result in tests][0]
            tests[name] = int(tests[name]) + 1
            result = self.connect.update_one({"name":id+"language"}, {'$set': tests})
            return result
        except (IndexError, ValueError):
            print(IndexError)
            print(ValueError)
            return 'Sorry, there are some errors in MongoDB.'
        
    def queryLog(self,name,id):
        # print(name)
        # print(id)
        try:
            tests = self.connect.find_one({"name":id+"language"})
            if tests is None:
                # return 'Sorry nothing found. Maybe you can try /GptON.'
                newID = {
                    "name":id+"language",
                    "javascript":0,
                    "python":0,
                    "java":0,
                    "c":0,
                    "c++":0,
                    "c#":0,
                    "css":0,
                    "html":0
                }
                self.connect.insert_one(newID)
                return self.queryLog(name,id)
            result = tests[name]
            return result
        except (IndexError, ValueError):
            # print(IndexError)
            # print(ValueError)
            return 'Sorry, there are some errors in MongoDB.'
        
# if __name__ == '__main__':
#     mongoTest = mongoDBconnect()
#     # result = mongoTest.readAlgorithm('binarysearch',"pythonImplementation")
#     # result = mongoTest.queryLog('javascript','123123123')
#     # result = mongoTest.increaseLog('javascript','123123123')
#     # result = mongoTest.queryLog('javascript')
#     print(result)


    