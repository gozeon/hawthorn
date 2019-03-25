import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='ddd',
    passwd='qwer1234',
    port='8889',
    # database='test_db',
    database='cardb',
)

mycursor = mydb.cursor()

# mycursor.execute('create database if not exists test_db')

# mycursor.execute("create table if not exists customers (name VARCHAR(255), address varchar(255))")
# message = {"name": "Tom", "address": "Beijing t"}
# sql = "insert into customers (name, address) values (%s, %s)"
# val = (message['name'], message['address'])
# mycursor.execute(sql, val)

# mydb.commit()


# sql = "insert into task (uuid,git_url,git_branch,npm_registry,docker_image,mail,"\
#     "status,jenkins_job_name,jenkins_build_number,jenkins_build_url,jenkins_build_result,"\
#     "dist_url) values (uuid(),'git@git.jdb-dev.com:pluto/h5_template.git','master',"\
#     "'https://registry.npm.taobao.org/','node',null, %s ,'pluto-h5_template',"\
#     "null,null,null,null)"
# val = ('activation',)
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.lastrowid)

# uuid = "cad8a188-49e9-11e9-bf49-6ad5ed24ec35"
# mycursor.execute("SELECT * FROM task where uuid = %s", (uuid,))
# myresult = mycursor.fetchone()
# if myresult:
#     print('to do update')
# else:
#     print('to do insert')

uuid = "9faa1de2-49ef-11e9-bf49-6ad5ed24ec35"
sql = "INSERT INTO customers (uuid, name, address)"\
    "VALUES (%s, %s, %s) "\
    "ON DUPLICATE KEY UPDATE address = values(address), name = values(name)"

mycursor.execute(sql, (uuid, None, '改',))
mydb.commit()
