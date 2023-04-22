#!/usr/bin/env python
import pika
import sys
import json
import ast
import mysql.connector
# print(mydb)
# c.execute("")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.18.0.2',heartbeat=0))
channel = connection.channel()
# channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
channel.queue_declare(queue='requestqueue')
# queue_name = result.method.queue
# channel.queue_bind(
        # exchange='direct_logs', queue=queue_name, routing_key="requestqueue")
print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    mydb = mysql.connector.connect(
  host="172.18.0.4",
  user="root",
  password="bhargav2652",
  database="Ccproject"
)
    c = mydb.cursor()
    dic=ast.literal_eval(body.decode('utf-8'))
    print(ast.literal_eval(body.decode('utf-8')))
    a=dic['name'][0]
    b=dic['SRN'][0]
    d=dic['section'][0]
    stmt=f'insert into students values("{a}" , "{b}" , "{d}")'
    print(stmt)
    c.execute(stmt)
    # c.execute("truncate table students")
    c.execute("select * from students")
    print(c.fetchall())
    print(properties.correlation_id)
    print(properties.reply_to)
    ch.basic_publish('',routing_key=properties.reply_to,body='successfully inserted tuple ('+a+','+b+','+d+')')
    print("ack sent")
    mydb.commit()
    #insert into dbms
channel.basic_consume('requestqueue',on_message_callback=callback)

channel.start_consuming()
