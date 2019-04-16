import docker
import json

client = docker.from_env()

container = client.containers.run('node',
                                  environment={
                                      "GIR_URL": "git@git.jdb-dev.com:pluto/h5_template.git",
                                      # "GIR_URL": "git@git.jdb-dev.com:fe/ditui-ajs.git",
                                      "GIR_BRANCH": "master",
                                      "NPM_REGISTRY": "https://registry.npm.taobao.org/",
                                      "API_UPLOAD_URL": "http://100.73.37.4:8081/api/files/upload",
                                  },
                                  command='/bin/bash -c "curl -sSl http://gist.test.x.com/paste/94/raw/ | sh"',
                                  remove=True)
stdout = container.decode('utf-8')
print(stdout)

last_line = stdout.splitlines()[-1]
print(last_line)
try:
    result = json.loads(last_line)
except json.JSONDecodeError:
    result = last_line

if 'status' in result and result['status'] == 'success':
    print('成功')
    print(result)
else:
    print('失败')
    print(result)
