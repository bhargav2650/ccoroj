from flask import Flask,render_template,request
import pika
import sys
import json
import uuid

# print(s)
# cred = pika.PlainCredentials('bhargav2650','bhargav2652')
# parameters=pika.ConnectionParameters(host='172.18.0.2',virtual_host="bhargav2650",credentials=cred)
# print(parameters)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.18.0.2',heartbeat=0))
channel = connection.channel()
# channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
replyq = channel.queue_declare(queue='replyqueue')
qname=replyq.method.queue
print(qname)
channel.queue_declare(queue="requestqueue")
channel.queue_declare(queue="requestqueue2")
channel.queue_declare(queue="requestqueue3")
channel.queue_declare(queue="requestqueue4")
channel.start_consuming()
app = Flask(__name__)
message = 'Hello World!'
@app.route('/<health_check_route>',methods=['GET'])
def index(health_check_route):
    #rabbitmq1
    # print(request.form)
    cor_id=str(uuid.uuid4())
    channel.basic_publish(exchange='', routing_key=health_check_route,properties=pika.BasicProperties(reply_to=replyq.method.queue,correlation_id=cor_id), body="check "+ health_check_route)
    # time.sleep(10)
    t=[]
    def func5(ch, method, properties,body):
        print(body)
        t.append(body)
        channel.stop_consuming()
    channel.basic_consume(qname,on_message_callback=func5)
    channel.start_consuming()
    return t[0]
    # return render_template('home.html')
@app.route("/create",methods=['GET','POST'])
def func1():
    if request.method=='GET':
        return render_template("create.html")
    else:
        #rabbitmq2
        # print(replyq.method.queue)
        print(request.form)
        cor_id=str(uuid.uuid4())
        channel.basic_publish(exchange='', routing_key='requestqueue',properties=pika.BasicProperties(reply_to=replyq.method.queue,correlation_id=cor_id), body=str(request.form.to_dict(flat=False)))
        # time.sleep(10)
        def func5(ch, method, properties,body):
            print(body)
            channel.stop_consuming()
        channel.basic_consume(qname,on_message_callback=func5)
        channel.start_consuming()
        return "hello thankyou"+request.form['SRN']+request.form['name']
@app.route("/read",methods=["GET"])
def func2():
    #rabbitmq3
    if request.method=='GET':
        #do database stuff using rabbitmq customer
        # print(request.form)
        cor_id=str(uuid.uuid4())
        channel.basic_publish(exchange='', routing_key='requestqueue2',properties=pika.BasicProperties(reply_to=replyq.method.queue,correlation_id=cor_id),body="hey gimme all records")
        # time.sleep(10)
        d=[]
        def func5(ch, method, properties,body):
            print(body)
            d.append(body)
            channel.stop_consuming()
        channel.basic_consume(qname,on_message_callback=func5)
        channel.start_consuming()
        # return "hello thankyou"+request.form['SRN']+request.form['name']
        return d[0]
        # return render_template("update.html")
@app.route("/delete/<srn>",methods=['GET'])
def func3(srn):
    # print(request.form)
    cor_id=str(uuid.uuid4())
    channel.basic_publish(exchange='', routing_key='requestqueue3',properties=pika.BasicProperties(reply_to=replyq.method.queue,correlation_id=cor_id), body=srn)
    # time.sleep(10)
    def func5(ch, method, properties,body):
        print(body)
        channel.stop_consuming()
    channel.basic_consume(qname,on_message_callback=func5)
    channel.start_consuming()
    # return "hello thankyou"+request.form['SRN']+request.form['name']
    #rabbitmq4 delete from db
    return srn
if __name__ == '__name__':
    app.run(host='0.0.0.0',debug=True)
app.run(host='0.0.0.0',debug=True)