# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:40:33 2019

@author: 18123
"""
class connect():    
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
    #print("Reducer ready")
    s.send(str.encode("Reducer Ready"))
#    time.sleep(2)
    #reducer()
    s.send(str.encode("Reducers' Task done"))

    
    
    
    def reducer(Config):
        file = open('intermediate_op2.txt')
        filename=Config['SectionOne']['filename']  #for inverted index
        reducer_op=[]
        reducer_inv=[]
        reducer_op2=[]
        for line in file:
            line=line.strip()
            x=line.split(" ")
            key=x[0]
            value=x[1]
            reducer_op.append((key,int(value)))
            #reducer_inv.append((key+'_'+filename,int(value)))
            
        #print(reducer_op)
        
        current_word = None
        current_count = 0
        word = None
        for element in reducer_op :
            word=element[0]
            count=element[1]
            
            if current_word == word:
                current_count += count
            else:
                if current_word:
                # Store it as key value pair
                    #print(current_word, current_count)
                    reducer_op2.append((current_word, current_count))
                    reducer_inv.append((current_word+'_'+filename,current_count))
                     
                current_count = count
                current_word = word
    
    # do not forget to output the last word if needed!
        if current_word == word:
            #print(current_word, current_count)
            reducer_op2.append((current_word, current_count))
            reducer_inv.append((current_word+'_'+filename,current_count))
        # Write it into file
        operation= Config['SectionOne']['operation']
        if operation == 'WordCount':
            with open('word_count.txt','a+') as fp:
                fp.write('\n'.join('%s %s' %x for x in reducer_op2))
        #writing inverted index output into file
        elif operation == 'InvertedIndex':
            with open('inverted_index.txt','a+') as fp1:
                fp1.write('\n'.join('%s %s' %x for x in reducer_inv))
            

    reducer(Config)  
        

