NAME = 'Database name'                  
USER = 'USER'
PASSWORD = 'PASSWORD'
HOST ='localhost'
con = None
# cur = None
# from tkinter import INSERT
import psycopg2
import psycopg2.extras
import pyttsx3 as textSpeach
from datetime import datetime,date

engine = textSpeach.init()
rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
engine.setProperty('rate', 155)  
"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[2].id)  

def present(name):
    try:
        with psycopg2.connect(host=HOST, user=USER,password=PASSWORD,database=NAME) as con:
            with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                create_table =''' Create table IF NOT EXISTS Empolyee (
                    ID  SERIAL PRIMARY KEY,
                    Name varchar(50) NOT NULL,
                    Date DATE NOT NULL,
                    Time TIME NOT NULL)'''
                cur.execute(create_table)
                exists = '''SELECT (name,date) FROM Empolyee WHERE (name='{}' AND date='{}')'''.format(name,date.today())
                cur.execute(exists)
                # result = cur.fetchone()
                ex=bool(cur.rowcount)
                # print(ex)
                if ex==True:
                    pass
                else:
                    insert = '''INSERT INTO Empolyee (Name,Date,Time) VALUES ('{}',CURRENT_DATE,CURRENT_TIME)'''.format(name)
                    print(name)
                    statment = str('Good morning' + name + 'have a nice day.')
                    engine.say(statment)
                    engine.runAndWait()
                    
                    
                # SELECT EXISTS(SELECT name FROM Customers WHERE City = 'Marseille');
                # insert = "INSERT INTO Empolye (name) VALUES ('{}'))".format(name)
                # cur.execute("INSERT INTO Empolye (Name, Image) VALUES ('{}', decode('{}', 'base64')))".format(emname, st))
                
                    cur.execute(insert)
                # cur.execute('''select name from Empolyee where Empolyee=%s'''.format(name))
                con.commit()
    except Exception as error:
        print(error)
    finally:
        # if cur is not None: 
        #     cur.close()
        if con is not None: 
            con.close()    
# print(name) 
# INSERT INTO contacts(contact_id, contact_name) SELECT supplier_id, supplier_name FROM suppliers WHERE EXISTS (SELECT 1
# FROM orders
# WHERE suppliers.supplier_id = orders.supplier_id);
