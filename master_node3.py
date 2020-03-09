# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 19:26:58 2019

@author: 18123
"""

import socket
import string
#import mapper
import time
from multiprocessing import Process
from threading import Thread
import configparser
from pprint import pprint
from oauth2client.client import GoogleCredentials

import os
import time

#import googleapiclient.discovery
from googleapiclient import discovery
from six.moves import input

Config = configparser.ConfigParser()
Config.read("config_file.ini")
Config.sections()

filename= Config['SectionOne']['filename'] 
doc = open(filename ,encoding='utf8')

#create socket
def create_socket():
    try:
        global host
        global port
        global s
        host= Config['SectionOne']['host']
        port= int(Config['SectionOne']['port'])
        s=socket.socket()
        
    except socket.error as msg:
        print("SERVER_ERROR Socket Not Created\r\n"+ str(msg))
        
#Binding the socket
def bind_socket():
    try:
        print("Binding the port " + str(port))
        s.bind((host,port))
        print("binded")
        s.listen(5)
        
    except socket.error as msg:
        print("socket binding Error "+ str(msg) + "\n" + "Retrying...")
        bind_socket()


#Accepting connections while listening
def accept_connections():
    global jobs
    jobs= []
    no_splits=3 # no of splits into the input file
   # p1=Thread(target=accepting_client,args=(s,))
   # p1.start()
   # p2=Thread(target=mapper_spawn)
   # p2.start()
    mapper_spawn()
    accepting_client(s)
    
       
        
    #reducer_spawn() #Calling reducer
def mapper_spawn():
#    import mapper
#    mapper.connect()
    #main("aman-kumar-257316", "ass4_bucket1", "us-central1-a", "mappers")
    num_map=4
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = 'aman-kumar-257316'
    zone = 'us-central1-a'
    instance = ['mapperreducer-1','mapperreducer-2', 'mapperreducer-3','kv-store']
    print("Starting all instances")
    for i in range(num_map):
        request = service.instances().start(project=project, zone=zone, instance=instance[i])
        response = request.execute()
        #pprint(response)
def reducer_spawn():
    import reducer
    reducer.connect()
def accepting_client(s):
    print("Accepting connections")
    while True:
        conn_obj,adress=s.accept() # executes until it accepts a connection
        print("Connection established with IP "+ adress[0] + " and port "+ str(adress[1]))
        send_commands(conn_obj)
 
    
    
    
# Sending file to mappers and reducers
def send_commands(conn_obj):
    
    rcvd_ack=str(conn_obj.recv(1024),"utf-8")
    print(rcvd_ack) # debugging
#send_filecontents
    z=[] #list of sentences
    for line in doc:
        line=line.strip() # strip with trailing and leading spaces
        z.append(line)    #list of string
    
    ip_string= ' '.join(z) #whole text as a single string
    ip_string=ip_string.translate(str.maketrans('', '', string.punctuation))  # removing punctutaions
    
    str_size = len(ip_string)
    part_size = int(str_size/3)
    str1=ip_string[:part_size]
    str2=ip_string[part_size+1:2*part_size]
    str3=ip_string[2*part_size+1:]
    
    conn_obj.send(bytes(ip_string,"utf-8")) # send data chunck to mapper
#    conn_obj.send(bytes(ip_string,"utf-8"))
#    conn_obj.send(bytes(ip_string,"utf-8"))

    
    rcvd_ack2=str(conn_obj.recv(1024),"utf-8")
    print(rcvd_ack2)
    
    time.sleep(2)
    
    ##Stopping instances##
    
    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)
    
    # Project ID for this request.
    project = 'aman-kumar-257316'  # TODO: Update placeholder value.
    
    # The name of the zone for this request.
    zone = 'us-central1-a'  # TODO: Update placeholder value.
    
    # Name of the instance resource to stop.
    instance = ['mapperreducer-2', 'mapperreducer-3','kv-store']  # TODO: Update placeholder value.
    
    print("stopping instances")
    
    for i in range(len(instance)):
        request = service.instances().stop(project=project, zone=zone, instance=instance[i])
        response = request.execute()
        #pprint(response)
    
    print("All instances stopped except mapperreducer-1")
   
    
   # reducer_spawn() #Calling reducer
    
#    ack_reducer=str(conn_obj.recv(1024),"utf-8")
#    print(ack_reducer)
    
    
# Calling functions
if __name__=="__main__":
    
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\18123\\AppData\\Local\\Google\\Cloud SDK\\google-cloud-sdk\\bin\\aman-kumar-07b279a83bcc.json'    
    create_socket()
    bind_socket()   
    accept_connections()
