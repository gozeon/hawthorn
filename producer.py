import pika
from configparser import ConfigParser, ExtendedInterpolation

import json
import scope

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config.ini')
# credentials = pika.PlainCredentials('admin', 'admin')
# connection = pika.BlockingConnection(pika.ConnectionParameters('100.73.48.248', '5672', '/', credentials))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config['AMPQ']['host']))

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

# message = {
#     'uuid': str(uuid.uuid4()),
#     # 'uuid': "00671b33-a479-4db2-badf-694699b636b0",
#     'git_url': 'git@git.jdb-dev.com:pluto/h5_template.git',
#     'git_branch': 'master',
#     'npm_registry': 'https://registry.npm.taobao.org/',
#     'docker_image': 'node',
#     'mail': None,
#     'status': 'activate',
#     'jenkins_job_name': None,
#     'jenkins_build_number': None,
#     'jenkins_build_url': None,
#     'jenkins_build_result': None,
#     'dist_url': None,
# }
# message = {
#   "uuid": "82c2b988-05c2-4db7-8f0c-959cb3524c71",
#   "docker_image": "node",
#   "status": "success",
#   "npm_registry": "https://registry.npm.taobao.org/",
#   "mail": "",
#   "git_url": "git@git.jdb-dev.com:pluto/h5_template.git",
#   "git_branch": "master",
#   "dist_url": "http://100.73.37.4/uploads/6917d52515ef83b10ac5f76ad9e01d5e52a9c08a.tar.gz",
#   "jenkins_build_number": 10,
#   "jenkins_build_url": "http://127.0.0.1:8080/job/pluto-h5_template/10/",
#   "jenkins_job_name": "pluto-h5_template",
#   "jenkins_build_result": "success"
# }


# channel.basic_publish(exchange=scope.exchange_dict['build'],
#                       routing_key='',
#                       body=json.dumps(message))
#
channel.close()


def publish(exchange, routing_key, messages, ):
    channel_private = connection.channel()

    # publish
    channel_private.basic_publish(exchange=exchange,
                                  routing_key=routing_key,
                                  body=json.dumps(messages))

    channel_private.close()
