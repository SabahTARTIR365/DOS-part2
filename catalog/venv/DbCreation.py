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
         
c.execute("INSERT INTO books VALUES(1 ,'How to get a good grade in DOS in 40 minutes a day' , 'distributed system' , 300 ,20 )")
c.execute("INSERT INTO books VALUES(2 ,'RBCs for Noobs' , 'distributed system' , 100 ,25 )")  
c.execute("INSERT INTO books VALUES(3 ,'HXen and the Art of Surviving Undergraduate School' , 'undergraduate school' , 600 ,60 )") 
c.execute("INSERT INTO books VALUES(4 ,'Cooking for the Impatent Undergrad' , 'undergraduate school' , 600 ,100 )")         
conn.commit()          

