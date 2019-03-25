import pika
import sys
import scope
import consumer_log
import consumer_mail
import consumer_result
import consumer_jenkins

parameters = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 创建队列
channel.queue_declare(queue=scope.queue_dict['log'],
                      durable=True)
channel.queue_declare(queue=scope.queue_dict['jenkins'],
                      durable=True)
channel.queue_declare(queue=scope.queue_dict['result'],
                      durable=True)
channel.queue_declare(queue=scope.queue_dict['mail'],
                      durable=True)
# 创建交换机
channel.exchange_declare(exchange=scope.exchange_dict['build'],
                         exchange_type='fanout')
channel.exchange_declare(exchange=scope.exchange_dict['built'],
                         exchange_type='fanout')
# 绑定
channel.queue_bind(exchange=scope.exchange_dict['build'],
                   queue=scope.queue_dict['log'])
channel.queue_bind(exchange=scope.exchange_dict['build'],
                   queue=scope.queue_dict['jenkins'])
channel.queue_bind(exchange=scope.exchange_dict['build'],
                   queue=scope.queue_dict['result'])
channel.queue_bind(exchange=scope.exchange_dict['build'],
                   queue=scope.queue_dict['mail'])

channel.queue_bind(exchange=scope.exchange_dict['built'],
                   queue=scope.queue_dict['log'])
channel.queue_bind(exchange=scope.exchange_dict['built'],
                   queue=scope.queue_dict['result'])
channel.queue_bind(exchange=scope.exchange_dict['built'],
                   queue=scope.queue_dict['mail'])


def callback(ch, method, properties, body):
    # print(ch)
    print(method.exchange)
    # print(properties)
    print(" [x] %r" % body)
    print(method.delivery_tag)
    # 消息确认，否则重启文件，会把原先的记录重新开启，no_ack 也是这样
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(consumer_log.callback, scope.queue_dict['log'])
channel.basic_consume(consumer_jenkins.callback, scope.queue_dict['jenkins'])
channel.basic_consume(consumer_result.callback, scope.queue_dict['result'])
channel.basic_consume(consumer_mail.callback, scope.queue_dict['mail'])

# channel.basic_consume(callback, scope.queue_dict['log'], no_ack=True)
# channel.basic_consume(callback, scope.queue_dict['jenkins'], no_ack=True)
# channel.basic_consume(callback, scope.queue_dict['result'], no_ack=True)
# channel.basic_consume(callback, scope.queue_dict['mail'], no_ack=True)

channel.start_consuming()
