# 开发

> 爱迪生说过：“要把BOSS打倒就要准备足够的等级。”

## 环境

### git

```bash
git clone git@git.jdb-dev.com:pluto/hawthorn.git
```

### python

version >= 3

```bash
pyenv activate v365 && virtualenv env && source env/bin/activate
```

### package

```bash
pip install -r requirements.txt
```

### mysql

```bash
# https://dev.mysql.com/doc/refman/8.0/en/mysql-batch-commands.html
mysql hawthorn < task.sql
```

### docker

[Install](https://www.docker.com/get-started)

### rabbitMQ

```bash
docker run --rm -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```

### jenkins

[Install](https://jenkins.io/doc/pipeline/tour/getting-started/)

## 配置

### jenkins配置

```bash
vim +12 consumer_jenkins.py
```

### rabbitMQ配置

```bash
vim +9 consumer.py
vim +7 producer.py
```

### mysql配置

```bash
vim +4 consumer_result.py
```

### smtp配置

```bash
vim +28 consumer_mail.py
```

### 其他

```bash
vim +12 consumer_jenkins.py
```

## 运行

### api server

```bash
FLASK_APP=server.py FLASK_ENV=development FLASK_DEBUG=1 flask run -h 0.0.0.0
```

### consumer server

```bash
python consumer.py
```
