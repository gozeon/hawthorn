import pika
import sys

parameters = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='test.logs',exchange_type='fanout')

message = 'hhh'
channel.basic_publish(exchange='test.logs', routing_key='', body=message)

print("[x] Sent %r" % message)

channel.close()
