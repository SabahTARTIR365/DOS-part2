from flask import Flask
from flask import request
import requests
import collections
app = Flask(__name__)
orderIpAddress= "192.168.1.14"
catalogIpAddress="192.168.1.70"

class LRUCache:
  def __init__(self, size):
    self.size = size
    self.lru_cache = collections.OrderedDict()
 
  def get(self, key):
    try:
      value = self.lru_cache.pop(key)
      self.lru_cache[key] = value
      return value
    except KeyError:
      return -1
 
  def put(self, key, value):
    try:
      self.lru_cache.pop(key)
    except KeyError:
      if len(self.lru_cache) >= self.size:
        self.lru_cache.popitem(last=False)
    self.lru_cache[key] = value

  def delete(self, key):
    try:
      self.lru_cache.pop(key)
    except KeyError:
      if len(self.lru_cache) >= self.size:
        self.lru_cache.popitem(last=False)
   
 
  def show_entries(self):
    print(self.lru_cache)


 

@app.route("/")
def hello():
  return "Hello World!"


# Search opearation
# return the books information( Item Number (ID),title) according to a  given topic
# this reqest send to the catalog server
@app.route('/search/<topic>', methods=['Get'])
def search(topic):
    response = requests.get("http://"+catalogIpAddress+":5000/search/" + topic)
    return response.content

# info opearation
# return  information about specific book according to given ID
# this req send to catalog server 
@app.route('/info/<int:id>', methods=['Get'])
def information_id(id):
    response = requests.get("http://"+catalogIpAddress+":5000/info/" + str(id))
    return response.content

# purchase opearation
#this post req will be sent to ORDER server in order to purchase specific book
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
    response = requests.post("http://"+orderIpAddress+":5000/purchase/" + str(id))
    return response.content

# this req will be used from the internal system by the admin in order to
#update price of specific book - it will send to catalog server
@app.route('/update_price/<int:id>', methods=['Put'])
def update_price(id):
    price = request.json['price']
    response = requests.put("http://"+catalogIpAddress+":5000/update_price/" + str(id), {'price': price})
    return response.content

if __name__ == "__main__":
    # Create an LRU Cache with a size of 3
  cache = LRUCache(3)
  app.run(debug=True, port=3500)