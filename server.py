import uuid
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from cerberus import Validator

import producer
import scope

v = Validator()

app = Flask(__name__)
Swagger(app)


@app.route('/', methods=['GET'])
def index():
    return """
    <a href="#">参考文档</a><br/>
    <a href="/apidocs">API 接口文档</a>
    """


@app.route('/general', methods=['POST'])
@swag_from('./apidoc/general.yml')
def general():
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
        # TODO send data to rabbitMQ
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
        # TODO send data to rabbitMQ
        producer.publish(scope.exchange_dict['built'], '', request.json)
        return jsonify(request.json), 201
    else:
        return jsonify(v.errors), 400


@app.route('/rpc', methods=['GET', 'POST'])
def rpc():
    return '接口暂未开放', 200
