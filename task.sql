create database if not exists hawthorn;
use hawthorn;
create table if not exists task
(
  id                   int auto_increment,
  uuid                 char(36)                                         null,
  git_url              varchar(2083)                                    null,
  git_branch           varchar(255)                                     null,
  npm_registry         varchar(255)                                     null,
  docker_image         varchar(255)                                     null,
  mail                 varchar(255)                                     null,
  status               enum ('activate', 'building', 'success', 'fail') null,
  jenkins_job_name     varchar(255)                                     null,
  jenkins_build_number int                                              null,
  jenkins_build_url    varchar(2083)                                    null,
  jenkins_build_result varchar(255)                                     null,
  dist_url             varchar(2083)                                    null,
  constraint task_id_uindex
  unique (id),
  constraint task_uuid_uindex
  unique (uuid)
);

alter table task
  add primary key (id);

