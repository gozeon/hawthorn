import pika
import sys

parameters = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='test.logs', exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='test.logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
  print(" [x] %r" % body)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
