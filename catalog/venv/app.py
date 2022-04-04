from flask import Flask,request
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
    
@app.route('/')
def my_app():
    return 'First Flask application!'
    
@app.route('/search/<topic>',methods=['GET'])
def searchTopic(topic):
       topic1 = topic.replace("%20"," ")

       query='select item_number,title from books where topic= "' + topic1+'"'
       rows = getFromDB(query)
       if(len(rows)==0) :
          return{'result ': 'unkown topic'}
       finalResult = []
       for i in rows :
          dic =dict( item_number= i[0],title = i[1])
          finalResult.append(dic)
       return {'result ':finalResult}



#search according to item number and return all info 
@app.route('/info/<int:number>',methods=['GET'])
def info(number):
    
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
              
              
@app.route('/count/<int:id>',methods=['GET'])
def getCount(id):
       
       query='select quantity from books where item_number= "' + str(id)+'"'
       rows = getFromDB(query)
       if(len(rows)==0) :
          return{'result ': 'unkown Book'}
       
       return str(rows[0][0])

             
@app.route('/update_amount/<int:id>',methods=['POST'])
def update(id):
   query = 'select * from books where item_number =  "' + str(id)+'"'
   rows = getFromDB(query)
   if(len(rows)==0) :
          return{'result ': 'update failed ,unkown Book Id'}
   amount = request.form.get('amount')     
   query='update books set quantity='+str(amount)+' where item_number= "' + str(id)+'"'
   rows = getFromDB(query)
       
   return{'result ': "update successed"}
    
#check if the book is excit and update the price (user from admin of the system)
@app.route('/update_price/<int:id>', methods=['Put'])
def update_price(id):
    sqlite_query1 = 'select * from books where item_number ='+str(id)
    rows1 = getFromDB(sqlite_query1)
    if len(rows1)== 0:
        return "Unkown Book"
    price = request.form.get('price')
    sqlite_query = 'update books set cost ='+str(price)+' where item_number ='+str(id)
    rows = getFromDB(sqlite_query)
    return "price updated sucsesfully"
      
              
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


if __name__ == '__main__':
    app.run(debug=True)
