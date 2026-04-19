from Lugwit_Module import lprint
import json

tableNameList={
    '用户列表': 'user_list',
    '组列表': 'group_list',
    '组用户列表': 'group_users',
    '用户权限': 'user_permissions',
    '组权限': 'group_permissions',
    '邮箱':"email",
    '用户名': "userName",
    '密码': "password",
    '用户ID': 'user_id',
    '组ID': 'group_id',
    '权限ID': 'permission_id',
    '用户权限列表': 'user_permission_list',
    '组权限列表': 'group_permission_list',
}

tnl=tableNameList

tables = {
    tnl["用户列表"]: """
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            is_leader BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """,
    tnl["组列表"]: """
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            description VARCHAR(255)

    """,
    tnl['组用户列表']: f"""
            {tnl['用户ID']} INT,
            {tnl['组ID']} INT,
            FOREIGN KEY ({tnl['用户ID']}) REFERENCES {tnl["用户列表"]}(id),
            FOREIGN KEY ({tnl['组ID']}) REFERENCES {tnl["组列表"]}(id),
            PRIMARY KEY ({tnl['用户ID']}, {tnl['组ID']})
    """,
    tnl['用户权限']: f"""
            {tnl['用户ID']} INT,
            {tnl['权限ID']} INT,
            FOREIGN KEY ({tnl['用户ID']}) REFERENCES {tnl['用户列表']}(id),
            FOREIGN KEY ({tnl['权限ID']}) REFERENCES {tnl['用户权限列表']}(id),
            PRIMARY KEY ({tnl['用户ID']}, {tnl['权限ID']})
        );
    """,
    tnl['组权限']: f"""       
            {tnl['组ID']} INT,
            {tnl['权限ID']} INT,
            FOREIGN KEY ({tnl['组ID']}) REFERENCES {tnl['组列表']}(id),
            FOREIGN KEY ({tnl['权限ID']}) REFERENCES {tnl['组权限列表']}(id),
            PRIMARY KEY ({tnl['组ID']}, {tnl['权限ID']})
    """
}

if __name__ == '__main__':

    def clean_sql(sql):
        # 去除换行符并替换多余的空格
        return ' '.join(sql.split())


    # 清理每个 SQL 语句
    cleaned_tables = {k: clean_sql(v) for k, v in tables.items()}

    # 打印格式化后的 JSON
    print(json.dumps(cleaned_tables, indent=4, ensure_ascii=False))
