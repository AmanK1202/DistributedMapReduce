# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:22:09 2019

@author: 18123
"""

def mapper_task(words):
    import time
    temp_list=[]
    for word in words:
                
        temp_list.append((word,1))  # Creating Key Value Pair
    temp_list.sort(key= lambda temp_list:temp_list[0]) #sorting the list by keys i.e combiner function
        # Setting the sorted key-value pair into file
    time.sleep(1) # To enable all multiple reducers to write onto the same file
    with open('intermediate_op2.txt','a+') as f:
        f.write('\n'.join('%s %s' % x for x in temp_list))

def spawn_reducers():
    import reducer
    reducer.connect()

           
    
def send_to_server(z):

    import TCP_Server
    import pickle
    msg = pickle.dumps(z)
    print(msg)
    s.send(bytes(msg,'utf-8'))
    

class connect1():
    
    import socket
    import time
    global s
    import configparser
    Config = configparser.ConfigParser()
    Config.read("config_file.ini")
    Config.sections()
    s=socket.socket()
    host=Config['SectionOne']['host']
    
    port= int(Config['SectionOne']['port'])
    #time.sleep(3)
    s.connect((host,port))
    #print("Mapper ready")
    ack = s.send(str.encode("Mapper Ready"))

    server_string = str(s.recv(10000000),"utf-8") # Recieved data from master node
    words=server_string.split() # get list of words
    #print(words)
    

    
    mapper_task(words)
    #sending ack back to master node
    ack2=s.send(str.encode("Mappers Task Done"))
    
    spawn_reducers()

    
    #s.close()
    
    


