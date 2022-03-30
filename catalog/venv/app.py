from flask import Flask
from flask_restful import Resource, Api
import sqlite3

app = Flask(__name__)
api = Api(app)


def getFromDB(stetment):
    #database connection
    sqliteConnection = sqlite3.connect('store.db')
    cursor = sqliteConnection.cursor()
    #execute sql quary
    count  = cursor.execute(stetment)
    rows = (cursor.fetchall())
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
    finalResult =[]
    return rows;
    

#search(topic)
class searchTopic(Resource):
    def get(self,topic):
       topic1 = topic.replace("%20"," ")

       query='select title,quantity from books where topic= "' + topic1+'"'
       rows = getFromDB(query)
       if(len(rows)==0) :
          return{'result ': 'unkown topic'}
       finalResult = []
       for i in rows :
          dic =dict(title = i[0],quantity = i[1])
          finalResult.append(dic)
       return {'result ':finalResult}



#search according to item number and return all info 
class info(Resource):
    def get(self,number):

       query='select * from books where item_number='+ str(number)
       rows =getFromDB(query)
       if(len(rows)==0) :
          return{'result ': 'no results for your query, please be sure you  entered valid item number '}
           
       finalResult = []
       for i in rows :
          dic =dict(item_number =i[0],title = i[1],topic= i[2] , quantity =
           i[3] , cost = i[4])
          finalResult.append(dic)
       return {'result ':finalResult}
              
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(searchTopic, '/search/<topic>')
api.add_resource(info, '/info/<int:number>')

if __name__ == '__main__':
    app.run(debug=True)

