import json
import mysql.connector
from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config.ini')

mydb = mysql.connector.connect(
    host=config['MYSQL']['host'],
    user=config['MYSQL']['user'],
    passwd=config['MYSQL']['password'],
    port=config['MYSQL']['port'],
    database=config['MYSQL']['database'],
)

mycursor = mydb.cursor()

mycursor.execute("""
create table if not exists task
(
	id int auto_increment primary key,
	uuid char(36) null,
	git_url varchar(2083) null,
	git_branch varchar(255) null,
	npm_registry varchar(2083) null,
	docker_image varchar(255) null,
	mail varchar(255) null,
	status enum('activate', 'building', 'success', 'fail') null,
	jenkins_job_name varchar(255) null,
	jenkins_build_number int null,
	jenkins_build_url varchar(2083) null,
	jenkins_build_result varchar(255) null,
	dist_url varchar(2083) null,
	constraint task_id_uindex
		unique (id),
	constraint task_uuid_uindex
		unique (uuid)
);
""", )


def callback(ch, method, properties, body):
    data = json.loads(body)
    mycursor.execute(
        """
        INSERT INTO task (uuid,
                          git_url,
                          git_branch,
                          npm_registry,
                          docker_image,
                          mail,
                          status,
                          jenkins_job_name,
                          jenkins_build_number,
                          jenkins_build_url,
                          jenkins_build_result,
                          dist_url)
        VALUES (%s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s)
        ON DUPLICATE KEY UPDATE git_url=values(git_url),
                                git_branch=values(git_branch),
                                npm_registry=values(npm_registry),
                                docker_image=values(docker_image),
                                mail=values(mail),
                                status=values(status),
                                jenkins_job_name=values(jenkins_job_name),
                                jenkins_build_number=values(jenkins_build_number),
                                jenkins_build_url=values(jenkins_build_url),
                                jenkins_build_result=values(jenkins_build_result),
                                dist_url=values(dist_url);
        """,
        (
            data['uuid'],
            data['git_url'] or None,
            data['git_branch'] or None,
            data['npm_registry'] or None,
            data['docker_image'] or None,
            data['mail'] or None,
            data['status'] or None,
            data['jenkins_job_name'] or None,
            data['jenkins_build_number'] or None,
            data['jenkins_build_url'] or None,
            data['jenkins_build_result'] or None,
            data['dist_url'] or None,
        )
    )
    mydb.commit()
    #     print(method.exchange)
    #     # print(properties)
    #     print(" [x] %r" % body)
    #     print(method.delivery_tag)
    # 消息确认，否则重启文件，会把原先的记录重新开启，no_ack 也是这样
    ch.basic_ack(delivery_tag=method.delivery_tag)
