import json
import sqlalchemy
import bcrypt
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 加载配置
with open('user_system_table.json', 'r') as file:
    config = json.load(file)

Base = declarative_base()

# 动态创建User类
class User(Base):
    __tablename__ = config['table_names']['user_table']
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)

# UserSystem类
class UserSystem:
    def __init__(self, host, user, password, db_name):
        engine_url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
        self.engine = sqlalchemy.create_engine(engine_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, username, password, email):
        session = self.Session()
        userExist = bool(session.query(User).filter_by(username=username).first())
        emailExist = bool(session.query(User).filter_by(email=email).first())
        if userExist or emailExist:
            return ("username {} exist--{},\n"
                "email {} exist--{}").format(username, userExist, email, emailExist)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password=hashed_password, email=email)
        session.add(new_user)
        session.commit()
        return True

    def get_user(self, username):
        session = self.Session()
        return session.query(User).filter_by(username=username).first()

    def check_password(self, input_password, stored_password):
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))

    def check_user_exist(self, username):
        session = self.Session()
        return session.query(User).filter_by(username=username).first() is not None

    def check_email_exist(self, email):
        session = self.Session()
        return session.query(User).filter_by(email=email).first() is not None

    def update_user(self, username, **kwargs):
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        if user:
            for key, value in kwargs.items():
                if key == 'password':
                    value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                setattr(user, key, value)
            session.commit()

    def delete_user(self, username):
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()

    def __del__(self):
        self.engine.dispose()