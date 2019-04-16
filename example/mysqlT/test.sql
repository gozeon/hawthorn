-- 创建
create table if not exists cardb.task
(
	id int auto_increment,
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
)
;

alter table cardb.task
	add primary key (id)
;

-- 添加修改
-- https://stackoverflow.com/questions/12639407/sql-if-exists-update-else-insert-syntax-error
INSERT INTO test_db.task (uuid,
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
VALUES ('c72ca7c2-4a12-11e9-a164-4b7a8119f994',
        'git@git.jdb-dev.com:pluto/h5_template.git',
        'master',
        'https://registry.npm.taobao.org/',
        'node',
        'liqs@x.com',
        'activate',
        null,
        null,
        null,
        null,
        null)
ON DUPLICATE KEY UPDATE git_url=values(git_branch),
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
