import pika
import json

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('100.73.48.248', '5672', '/', credentials))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

message = {'id': 1, 'name': 'name1'}
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=json.dumps(message))

print("[x] Sent 'Hello World!'")

channel.close()
