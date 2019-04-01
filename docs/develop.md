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

see `config.ini`

```ini
[COMMON]
ip =

[AMPQ]
host = localhost
user = guest
password = guest
url = amqp://${AMPQ:user}:${AMPQ:password}@${AMPQ:host}

[JENKINS]
url = http://localhost:8080
user = admin
password = qwer1234

[API]
upload = http://100.73.37.4:8081/api/files/upload
download = http://100.73.37.4/uploads/
result = http://${COMMON:ip}:5000/result

[MYSQL]
host = localhost
user = ddd
password = qwer1234
port = 8889
database = test_db

[SMTP]
user =
password =
host = smtp.exmail.qq.com
port = 587
smtp_ssl = False


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

### rpc service

```bash
nameko run rpc_service --broker amqp://guest:guest@localhost
```
