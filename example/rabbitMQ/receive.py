import pika
import json

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('100.73.48.248', '5672', '/', credentials))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % json.loads(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
