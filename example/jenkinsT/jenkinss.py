import re
import os
import jenkins
import xml.etree.ElementTree as ET

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

server = jenkins.Jenkins('http://localhost:8080', username='admin', password='qiankun.230')
user = server.get_whoami()
version = server.get_version()

print('Hello %s from Jenkins %s' % (user['fullName'], version))

# my_job = server.get_job_config('asd')
# print(my_job)

def convert_xml_file_to_str():
  tmplXML = os.path.join(ROOT_DIR, 'tmpl.xml')
  tree = ET.parse(tmplXML)
  root = tree.getroot()
  return ET.tostring(root, encoding='utf8', method='xml').decode()

config = convert_xml_file_to_str()

def create_job_config(config_tpl, git_url, branch='master',docker_image='node', npm_registry='https://registry.npmjs.org/'):
  # https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
  rep = {
    "GIT_URL": git_url,
    "GIT_BRANCH": branch,
    "DOCKER_IMAGE": docker_image,
    "NPM_REGISTRY": npm_registry,
  }
  rep = dict((re.escape(k), v) for k, v in rep.items())
  pattern = re.compile("|".join(rep.keys()))
  new_config = pattern.sub(lambda m: rep[re.escape(m.group(0))], config_tpl)
  return new_config

config = create_job_config(config_tpl=config,
git_url='git@git.jdb-dev.com:pluto/h5_template.git',
npm_registry='https://registry.npm.taobao.org/')

# print(server.get_job_config('asd'))
server.delete_job('empty-asd')

server.create_job('empty-asd', config)
# jobs = server.get_jobs()
# print(jobs)

# queue_id = server.build_job('empty')
# print(queue_id)

# a = server.get_queue_info()
# a = server.get_queue_item(queue_id)
# current_build_number = None
# current_build_url = None
# 如果队列一直进不去，就会阻塞在这里
# 如果直接获取nextBuildNumber，会发生一个不可控的问题，比如：其他地方开始了build任务，这样build number就不准确了
# 可能比较好的方式就是手动设置build number，依赖插件 https://wiki.jenkins.io/display/JENKINS/Next+Build+Number+Plugin
# https://stackoverflow.com/questions/45472604/get-jenkins-job-build-id-from-queue-id/45474120
# while(current_build_number is None):
#   if 'executable' in server.get_queue_item(queue_id):
#     current_build_number = server.get_queue_item(queue_id)['executable']['number']
#     current_build_url = server.get_queue_item(queue_id)['executable']['url']
#   else:
#     continue

# print(current_build_number, current_build_url)


# jobs = server.get_jobs()
# print(jobs)


# next_buil_number = server.get_job_info('empty')['nextBuildNumber']
# last_build_number = server.get_job_info('empty')['lastCompletedBuild']['number']
# build_info = server.get_build_info('empty', 1)
# print(build_info)
# print(next_buil_number)

# print(server.get_all_jobs())

# server.delete_job('empty')

# print(server.job_exists('empty'))
