import sqlite3


#connect to db 
conn = sqlite3.connect('store.db')

c = conn.cursor();
c.execute("INSERT INTO books VALUES(5 ,'. How to finish Project 3 on time' , 'spring' , 300 ,150 )")
c.execute("INSERT INTO books VALUES(6 ,'Why theory classes are so hard' ,  'spring' , 100 ,125 )")  
c.execute("INSERT INTO books VALUES(7 ,'Spring in the Pioneer Valley' , 'spring' , 600 ,50 )") 