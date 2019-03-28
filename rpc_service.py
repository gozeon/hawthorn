import json

import docker
from nameko.rpc import rpc


class TaskService(object):
    name = 'hawthorn'

    @rpc
    def build(self,
              environment,
              docker_image='node',
              bash_file='http://gist.test.jiedaibao.com/paste/94/raw/'
              ):
        """
        environment={
            "GIR_URL": "git@git.jdb-dev.com:pluto/h5_template.git",
            "GIR_BRANCH": "master",
            "NPM_REGISTRY": "https://registry.npm.taobao.org/",
            "API_UPLOAD_URL": "http://100.73.37.4:8081/api/files/upload",
        },
        """
        client = docker.from_env()

        container = client.containers.run(docker_image,
                                          environment=environment,
                                          command='/bin/bash -c "curl -sSl {} | sh"'.format(bash_file),
                                          remove=True)
        stdout = container.decode('utf-8')
        last_line = stdout.splitlines()[-1]
        try:
            result = json.loads(last_line)
        except json.JSONDecodeError:
            result = last_line
        if 'status' in result and result['status'] == 'success':
            return result
        else:
            return {"status": "fail"}
