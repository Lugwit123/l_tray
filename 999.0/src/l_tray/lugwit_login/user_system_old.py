
import pymysql
import bcrypt
import user_system_tables
from Lugwit_Module import lprint
import traceback


class UserSystem:
    def __init__(self, host, user, password, db_name='', table_name=""):
        self.db_name = db_name
        # 初始连接时可能不指定数据库
        self.connection = pymysql.connect(host=host, user=user, password=password)
        self.cursor = self.connection.cursor()
        self.tableNameList=user_system_tables.tableNameList
        if db_name:
            self.create_database(db_name)  # 创建或切换到指定数据库
            
    def initTableNameList(self):
        self.userListColName=self.tableNameList['用户列表']
        self.groupListColName=self.tableNameList['组列表']
        self.groupUserListColName=self.tableNameList['组用户列表']
        self.userPermissionColName=self.tableNameList['用户权限']
        self.groupPermissionColName=self.tableNameList['组权限']
        self.emailColName=self.tableNameList['邮箱']
        self.userNameColName=self.tableNameList['用户名']
        self.passwordColName=self.tableNameList['密码']
        user_system_tables.tableNameList=self.tableNameList
            
    def init_userSystemTables(self):
        self.setup_tables()  # 创建表cursor.execute("USE your_database")

    def create_database(self,db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        self.cursor.execute(f"USE {db_name};")
        
    def create_table(self, table_name, table_schema):
        if not self.check_table_exists(table_name):
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({table_schema});')
            self.connection.commit()
        else:
            self.cursor.execute(f'USE {self.db_name};')
        
    def setup_tables(self):
        if not self.db_name:
            return
        tables=user_system_tables.tables
        # 遍历并创建所有表格
        for table_name, table_schema in tables.items():
            self.addOrUpdateTable(table_name, table_schema)

    def add_user(self, username, password, email):
        userExist=False;emailExist=False
        if self.checkEmailExist(email):
            print("Email already exist")
            userExist=True
        if self.checkUserExist(username):
            print("User already exist")
            emailExist=True
        if any([userExist ,emailExist]):
            return 'userExist- {userExist}\nEmailExist- {emailExist}'
        if not (8 <= len(password) <= 20):
            raise ValueError('Password must be between 8 and 20 characters long')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = f'INSERT INTO {self.userListColName} \
            ({self.userNameColName}, {self.passwordColName}, {self.emailColName}) \
                VALUES (%s, %s, %s);'
        self.cursor.execute(sql, (username, hashed_password, email))
        self.connection.commit()

    def get_user(self, username):
        sql = f'SELECT * FROM {self.userListColName} WHERE username = %s;'
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone()

    def check_password(self, input_password, stored_password):
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))
    
    
    def checkUserExist(self,user):
        # 假设你要检查的用户名
        username_to_check = user

        # 创建 SQL 查询
        sql = f"SELECT * FROM {self.userListColName} WHERE {self.userNameColName} = %s"

        # 执行查询
        self.cursor.execute(sql, (username_to_check,))

        # 检查是否有返回结果
        return self.cursor.fetchone()

    def checkEmailExist(self,email):
        # 假设你要检查的用户名
        email_to_check = email

        # 创建 SQL 查询
        sql = f"SELECT * FROM {self.userListColName} WHERE {self.emailColName} = %s"

        # 执行查询
        self.cursor.execute(sql, (email_to_check,))

        # 检查是否有返回结果
        return self.cursor.fetchone()
    
    def check_table_exists(self, table_name):
        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        result = self.cursor.fetchone()
        return result is not None
    
    def addOrUpdateTable(self,table_name,table_structure,rebuild_PRIMARYKEY=False):
        if not self.check_table_exists(table_name):#  CREATE TABLE IF NOT EXISTS group_permissions (
            columns = table_structure.strip().split(',\n')
            for i,col in enumerate(columns):
                columns[i] = col.strip()
            cmd=[x+',' for x in columns][0][:-1]
            cmd=f"CREATE TABLE IF NOT EXISTS {table_name} ({cmd});"
            lprint (cmd)
            self.cursor.execute(cmd)
        else:
            lprint (table_structure.strip())
            columns = table_structure.strip().split(',\n')
            for i,col in enumerate(columns):
                columns[i] = col.strip()
                columns[i] = columns[i].split('\n')[0]
            lprint (columns)
            for col in columns:
                # 提取列名
                lprint (col)
                col_name = col.split(' ')[0]
                alter_sql_list=[]
                # 检查列是否存在
                self.cursor.execute(
                    f"SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA \
                        = '{self.db_name}' AND TABLE_NAME = \
                        '{table_name}' AND COLUMN_NAME = '{col_name}'")
                column_exists = self.cursor.fetchone() is not None
                col_exists_cmd = 'MODIFY' if column_exists else 'ADD'
                if ' PRIMARY KEY' in col:
                    if not self.mainKeyExist(table_name):
                        alter_sql = f"ALTER TABLE {table_name} ADD {col}"
                        alter_sql_list+=[alter_sql]
                        lprint ('alter_sql_list-->>',alter_sql_list)
                    else:
                        if rebuild_PRIMARYKEY:
                            # 如果是主键并且重建主键则先删除主键在添加主键
                            alter_sql_A = f'ALTER TABLE {table_name} DROP PRIMARY {col_name}'
                            alter_sql_B = f"ALTER TABLE {table_name} ADD {col}"
                            alter_sql_list+=[alter_sql_A,alter_sql_B]
                            lprint ('alter_sql_list-->>',alter_sql_list)
                        elif not rebuild_PRIMARYKEY:
                            alter_sql=col.replace(" PRIMARY KEY",'')
                            alter_sql_list+=[f'ALTER TABLE {table_name} {col_exists_cmd} {alter_sql}']
                            lprint ('alter_sql_list-->>',alter_sql_list)
                else:#ALTER TABLE user_list MODIFY
                    alter_sql = f"ALTER TABLE {table_name} {col_exists_cmd} {col}"
                    alter_sql_list+=[alter_sql]
                    lprint ('alter_sql_list-->>',alter_sql_list)
                alter_sql_list=[x+';' for x in alter_sql_list][0]
                lprint ('alter_sql_list-->>',alter_sql_list)
                try:
                    self.cursor.execute(alter_sql_list)
                except pymysql.err.OperationalError:
                    print ('pymysql.err.OperationalError')
                
    def mainKeyExist(self,table_name):
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM information_schema.TABLE_CONSTRAINTS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = %s 
            AND CONSTRAINT_TYPE = 'PRIMARY KEY'
        """, (self.db_name, table_name))

        primary_key_exists = self.cursor.fetchone() is not None
        return primary_key_exists
    def __del__(self):
        self.connection.close()
