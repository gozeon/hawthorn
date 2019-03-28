import uuid
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from cerberus import Validator
from nameko.standalone.rpc import ClusterRpcProxy

import producer
import scope
import utils

v = Validator()

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


@app.route('/', methods=['GET'])
def index():
    return """
    <a href="http://100.73.39.79:81/#/">使用文档</a><br/>
    <a href="/apidocs">API 接口文档</a>
    """


@app.route('/general', methods=['POST'])
@swag_from('./apidoc/general.yml')
def general():
    """
    TODO: use cerberus default
    link: http://docs.python-cerberus.org/en/stable/normalization-rules.html#default-values
    """
    default_data = {
        "uuid": str(uuid.uuid4()),
        "docker_image": "node",
        "git_branch": "master",
        "npm_registry": "https://registry.npm.taobao.org/",
        "status": "activate",
        "jenkins_build_number": None,
        "jenkins_build_result": None,
        "jenkins_build_url": None,
        "jenkins_job_name": None,
        "mail": None,
        "dist_url": None,
    }
    schema = {
        'git_url': {
            'type': 'string',
            'required': True
        }
    }
    v.allow_unknown = True
    if v.validate(request.json, schema):
        message = {**default_data, **request.json}
        producer.publish(scope.exchange_dict['build'], '', message)
        return jsonify(message), 200
    else:
        return jsonify(v.errors), 400


@app.route('/result', methods=['POST'])
@swag_from('./apidoc/result.yml')
def result():
    schema = {
        'uuid': {'type': 'string', 'required': True},
        'git_url': {'type': 'string', 'required': True},
        'git_branch': {'type': 'string', 'required': True},
        'docker_image': {'type': 'string', 'required': True},
        'npm_registry': {'type': 'string', 'required': True},
        'mail': {'type': 'string', 'required': True, },
        'status': {'type': 'string', 'allowed': ['activate', 'building', 'success', 'fail'], 'required': True},
        'jenkins_build_number': {'type': 'integer', 'required': True, },
        'jenkins_build_result': {'type': 'string', 'required': True, },
        'jenkins_build_url': {'type': 'string', 'required': True, },
        'jenkins_job_name': {'type': 'string', 'required': True, },
        'dist_url': {'type': 'string', 'required': True, },
    }
    v.allow_unknown = False
    if v.validate(request.json, schema):
        producer.publish(scope.exchange_dict['built'], '', request.json)
        return jsonify(request.json), 201
    else:
        return jsonify(v.errors), 400


@app.route('/rpc', methods=['POST'])
@swag_from('./apidoc/rpc.yml')
def rpc():
    schema = {
        'git_url': {'type': 'string', 'required': True},
        'git_branch': {'type': 'string', 'default': 'master'},
        'docker_image': {'type': 'string', 'default': 'node'},
        'npm_registry': {'type': 'string', 'default': 'https://registry.npm.taobao.org/'},
        'api_upload_url': {'type': 'string', 'default': 'http://100.73.37.4:8081/api/files/upload'},
    }
    v.allow_unknown = False
    if v.validate(request.json, schema):
        data = v.normalized(request.json, schema)
        docker_image = data['docker_image']
        environment = utils.upper_key_dict(data)
        # noinspection PyBroadException
        try:
            with ClusterRpcProxy(CONFIG) as n:
                # asynchronously spawning the build task
                # https://stackoverflow.com/questions/40775709/avoiding-too-broad-exception-clause-warning-in-pycharm?answertab=active#tab-top
                build_result = n.hawthorn.build.call_async(environment=environment, docker_image=docker_image).result()
                return jsonify(build_result), 200
        except Exception as e:
            return jsonify({'message': '请联系管理员', 'info': str(e)}), 500

    else:
        return jsonify(v.errors), 400
