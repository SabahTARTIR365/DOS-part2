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
    return {'result ':rows}



class searchTopic(Resource):
    def get(self,topic):
       topic1 = topic.replace("%20"," ")
       
       query='select title,quantity from books where topic= "' + topic1+'"'
       return getFromDB(query)
       


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(searchTopic, '/search/<topic>')

if __name__ == '__main__':
    app.run(debug=True)

