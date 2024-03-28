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
    def increaseLog(self,name):
        try:
            tests = self.connect.find_one({"name":"language"})
            if tests is None:
                return 'Sorry nothing found. Maybe you can try /GptON.'
            # result = [result[name] for result in tests][0]
            tests[name] = int(tests[name]) + 1
            result = self.connect.update_one({"name":"language"}, {'$set': tests})
            return result
        except (IndexError, ValueError):
            print(IndexError)
            print(ValueError)
            return 'Sorry, there are some errors in MongoDB.'
    def queryLog(self,name):
        try:
            tests = self.connect.find_one({"name":"language"})
            if tests is None:
                return 'Sorry nothing found. Maybe you can try /GptON.'
            result = tests[name]
            return result
        except (IndexError, ValueError):
            print(IndexError)
            print(ValueError)
            return 'Sorry, there are some errors in MongoDB.'
        
# if __name__ == '__main__':
#     mongoTest = mongoDBconnect()
#     result = mongoTest.readAlgorithm('binarysearch',"pythonImplementation")
#     # result = mongoTest.queryLog('javascript')
#     # result = mongoTest.increaseLog('javascript')
#     # result = mongoTest.queryLog('javascript')
#     print(result)


    