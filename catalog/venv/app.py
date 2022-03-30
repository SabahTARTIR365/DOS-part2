from flask import Flask
from flask_restful import Resource, Api
import sqlite3

#connect to db 
conn = sqlite3.connect('store.db')
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

