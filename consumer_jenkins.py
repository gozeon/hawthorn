import re
import os
import json
import jenkins
import xml.etree.ElementTree as ET
from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config.ini')

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
API_UPLOAD_URL = config['API']['upload']
API_RESULT_URL = config['API']['result']
BASE_DOWNLOAD_URL = config['API']['download']
XML_TEMPLATE_FILE = 'template.xml'
server = jenkins.Jenkins(config['JENKINS']['url'],
                         username=config['JENKINS']['user'],
                         password=config['JENKINS']['password'])


def create_job_name(git_url):
    return (git_url.split(':').pop())[:-4].replace('/', '-')


def convert_xml_file_to_str():
    tmplXML = os.path.join(ROOT_DIR, XML_TEMPLATE_FILE)
    tree = ET.parse(tmplXML)
    root = tree.getroot()
    return ET.tostring(root, encoding='utf8', method='xml').decode()


def create_job_config(config_tpl,
                      git_url,
                      uuid,
                      mail,
                      branch='master',
                      docker_image='node',
                      npm_registry='https://registry.npmjs.org/'):
    # https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
    rep = {
        "GIT_URL": git_url,
        "GIT_BRANCH": branch,
        "DOCKER_IMAGE": docker_image,
        "NPM_REGISTRY": npm_registry,
        "API_UPLOAD_URL": API_UPLOAD_URL,
        "API_RESULT_URL": API_RESULT_URL,
        "BASE_DOWNLOAD_URL": BASE_DOWNLOAD_URL,
        "MAIL": mail,
        "UUID": uuid,
    }
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    new_config = pattern.sub(lambda m: rep[re.escape(m.group(0))], config_tpl)
    return new_config

# print(server.get_job_config('json'))


config_tpl = convert_xml_file_to_str()


def callback(ch, method, properties, body):
    data = json.loads(body)
    config = create_job_config(config_tpl=config_tpl,
                               git_url=data['git_url'],
                               branch=data['git_branch'],
                               uuid=data['uuid'],
                               mail=data['mail'],
                               docker_image=data['docker_image'],
                               npm_registry=data['npm_registry'])

    job_name = create_job_name(data['git_url'])
    if server.job_exists(job_name):
        # update job config
        server.reconfig_job(job_name, config)
    else:
        # create job
        server.create_job(job_name, config)
    server.build_job(job_name)
    # 消息确认，否则重启文件，会把原先的记录重新开启，no_ack 也是这样
    ch.basic_ack(delivery_tag=method.delivery_tag)
