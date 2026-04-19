from user_system import UserSystem

# 数据库配置，请根据你的数据库信息进行修改
# 数据库连接信息
db_host = 'localhost'  # 数据库服务器地址
db_user = 'root'  # 数据库用户名
db_password = '123456'  # 数据库密码
db_name = 'userSystem'  # 数据库密码

user_system = UserSystem(db_host, db_user, db_password, db_name)
user_system.add_user('username', 'password', 'email@example.com')
