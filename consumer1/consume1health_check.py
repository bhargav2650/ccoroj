#!/usr/bin/env python
import pika
import sys
import json
import ast
import mysql.connector
# c.execute("")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.18.0.2',heartbeat=0))
channel = connection.channel()

# channel.exchange_declare(exchange='topic_logs', exchange_type='direct')
# channel.queue_declare(queue='requestqueue')
# channel.queue_declare(queue='requestqueue2')
channel.queue_declare(queue='requestqueue4')
# queue_name = result.method.queue

# channel.queue_bind(
        # exchange='direct_logs', queue=queue_name, routing_key="requestqueue")

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    
    # print(c.fetchall())
    # print(properties.correlation_id)
    # print(properties.reply_to)
    ch.basic_publish('',routing_key=properties.reply_to,body="acknowledged "+ str(body))
    print("ack sent")
    print(body)
    # mydb.commit()
    #insert into dbms
channel.basic_consume('requestqueue4',on_message_callback=callback)
channel.start_consuming()
