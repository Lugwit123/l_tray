
def checkUserExist(cursor,user):
    # 假设你要检查的用户名
    username_to_check = user

    # 创建 SQL 查询
    sql = "SELECT * FROM users WHERE username = %s"

    # 执行查询
    cursor.execute(sql, (username_to_check,))

    # 检查是否有返回结果
    return cursor.fetchone()

def checkEmailExist(cursor,email):
    # 假设你要检查的用户名
    email_to_check = email
``
    # 创建 SQL 查询
    sql = "SELECT * FROM users WHERE email = %s"

    # 执行查询
    cursor.execute(sql, (email_to_check,))

    # 检查是否有返回结果
    return cursor.fetchone()