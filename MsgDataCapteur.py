#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pika, os
sys.path.append('/home/pi/Documents/TestTabbitmq/Sources')
from yocto_api import *

# connexion capteur
errmsg=YRefParam()
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS: sys.exit(errmsg.value)
sensor=YSensor.FindSensor("TMPSENS1-6292A.temperature")
if not sensor.isOnline() : sys.exit("device not found")

#lecture en boucle 
while sensor.isOnline():
	#lecture du capteur
	print("Temp :  " + "%2.1f" % sensor.get_currentValue() + "°C (Ctrl-C to stop)")
	#envoi des donnees par message rabbitmq

	credentials = pika.PlainCredentials("Site1","Site1")
	conn_params = pika.ConnectionParameters("localhost",credentials = credentials)
	conn_broker = pika.BlockingConnection(conn_params)
	channel = conn_broker.channel()
	channel.exchange_declare(exchange="CapteursData",type="fanout",passive=False,durable=True,auto_delete=False)
	msg_props = pika.BasicProperties()
	msg_props.content_type  = "text/plain"
	msg = ("Temp :  " + "%2.1f" % sensor.get_currentValue() + "°C ")
	channel.basic_publish(body=msg,exchange="CapteursData",properties=msg_props,routing_key="hola")
	print(" -> message parti")
	YAPI.Sleep(1000)
	
