import sqlite3


#connect to db 
conn = sqlite3.connect('store.db')

c = conn.cursor();

#db structure
c.execute("""CREATE TABLE books 
          (item_number INTEGER ,
          title text, 
          topic text,
          quantity INTEGER,
          cost REAL)""")
          
conn.commit()          

