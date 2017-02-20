#!/usr/bin/python
# _*_ coding: utf-8 _*_
import pika
credentials = pika.PlainCredentials("SiteInternet", "SiteInternet")
conn_params = pika.ConnectionParameters("ch4pi1.ddns.net",
                                        credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params) #/Establish connection to broker
channel = conn_broker.channel() #/Obtain channel

channel.exchange_declare(exchange="CapteursData", #/Declare the exchange
                         type="fanout",
                         passive=False,
                         durable=True,
                         auto_delete=False)

channel.queue_declare(queue="CapteursData") #/Declare the queue
channel.queue_bind(queue="AffichageInternet",     #/Bind the queue and exchange together on the key "hola"
                   exchange="CapteursData",
                   routing_key="hola")

def msg_consumer(channel, method, header, body): #/Make function to process incoming messages
    
    channel.basic_ack(delivery_tag=method.delivery_tag)  #/Message acknowledgement

    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer") #/Stop consuming more messages and quit
        channel.stop_consuming()
    else:
        print body
    
    return

channel.basic_consume( msg_consumer,    #/subscribe our consumer
                       queue="AffichageInternet",
                       consumer_tag="hello-consumer")
channel.start_consuming() #/Start consuming
