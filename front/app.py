from flask import Flask
from flask import request
import requests
app = Flask(__name__)
orderIpAddress= "192.168.1.14"
catalogIpAddress="192.168.1.70"

Port1 = 5000
Port2 = 4000

catalog_counter = 1 
order_counter = 1 
def catalog_round_robin():
    global catalog_counter
    #round robin between catalog servers 
    if(catalog_counter ==1):
      port=Port1
      catalog_counter = 2
    if(catalog_counter ==2):
      port=Port2
      catalog_counter = 1
    return  port

def order_round_robin():
    global order_counter
    #round robin between catalog servers 
    if(order_counter ==1):
      port=Port1
      order_counter = 2
    if(order_counter ==2):
      port=Port2
      order_counter = 1  
    return  port
     
@app.route("/")
def hello():
  return "Hello World!"


# Search opearation
# return the books information( Item Number (ID),title) according to a  given topic
# this reqest send to the catalog server
@app.route('/search/<topic>', methods=['Get'])
def search(topic):
    port=catalog_round_robin()
    response = requests.get("http://"+catalogIpAddress+":"+port+"/search/" + topic)
    return response.content
  
# info opearation
# return  information about specific book according to given ID
# this req send to catalog server 
@app.route('/info/<int:id>', methods=['Get'])
def information_id(id):
    port=catalog_round_robin()
    response = requests.get("http://"+catalogIpAddress+":"+port+"/info/" + str(id))
    return response.content

# purchase opearation
#this post req will be sent to ORDER server in order to purchase specific book
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
    port=order_round_robin()
    response = requests.post("http://"+orderIpAddress+":"+port+"/purchase/" + str(id))
    return response.content

# this req will be used from the internal system by the admin in order to
#update price of specific book - it will send to catalog server
@app.route('/update_price/<int:id>', methods=['Put'])
def update_price(id):
    port=catalog_round_robin()
    price = request.json['price']
    response = requests.put("http://"+catalogIpAddress+":"+port+"/update_price/" + str(id), {'price': price})
    return response.content

if __name__ == "__main__":
  app.run(debug=True)