from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from user_system import UserSystem  # 假设UserSystem在user_system.py中定义

app = FastAPI()

# 假设数据库连接信息
db_host = 'localhost'  # 数据库服务器地址
db_user = 'root'  # 数据库用户名
db_password = '123456'  # 数据库密码
db_name = 'userSystem'  # 数据库密码


user_system = UserSystem(db_host, db_user, db_password, db_name)

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/register/")
async def register(user: UserCreate):
    add_user_result = user_system.add_user(user.username, user.password, user.email)
    if add_user_result ==True:
        return {"message": "User created successfully."}
    else:
        raise HTTPException(status_code=400, detail=add_user_result)

@app.post("/login/")
async def login(user: UserLogin):
    db_user = user_system.get_user(user.username)
    if not db_user or not user_system.check_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "User logged in successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
