import sqlite3


class Mysqlite(object):
    def __init__(self, dbpath):
        # 如果不存在则创建
        self.con = sqlite3.connect(dbpath)
        self.cur = self.con.cursor()

    def __del__(self):
        self.close()

    def execute_sqlite3(self, sql):
        # 命令处理
        sql = sql.lower()
        if 'insert' in sql or 'delete' in sql or 'update' in sql:
            self.cur.execute(sql)
            self.con.commit()
            # print('done..')
            return
        elif 'max' in sql:
            self.cur.execute(sql)
            data = str(self.cur.fetchone())
            return data
        elif 'select' in sql:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            # print(data)
            return data

    def insert_value(self, table_name, value):
        # 插入自定义数据
        sql = "INSERT INTO {} values({})".format(table_name, value)
        self.execute_sqlite3(sql)

    def select_data(self, table_name):
        # 查询数据
        sql = "SELECT * FROM {}".format(table_name)
        data = self.execute_sqlite3(sql)
        return data

    def select_data2(self, table_name, condition):
        # 查询数据
        sql = "SELECT * FROM {} WHERE {}".format(table_name, condition)
        data = self.execute_sqlite3(sql)
        return data

    def select(self, sql):
        # 查询数据
        data = self.execute_sqlite3(sql)
        return data

    def select_count(self, table_name, condition):
        # 查询数据数量
        sql = "SELECT count(*) FROM {} WHERE {}".format(table_name, condition)
        num = self.execute_sqlite3(sql)
        return num

    def update_data(self, table_name, field, value, id):
        # 修改数据
        sql = "UPDATE {} set {} = '{}' where id = {}".format(table_name, field, value, id)
        self.execute_sqlite3(sql)

    def delete_data(self, table_name, where):
        # 删除数据
        sql = "DELETE FROM {} where {}".format(table_name, where)
        self.execute_sqlite3(sql)

    def close(self):
        # 关闭资源
        self.cur.close()
        self.con.close()

# if __name__ == "__main__":
#     sqlite = Mysqlite('test.db')
#     table_name = 'foo'
#     try:
#         sqlite.create_table(table_name, 'id integer primary key autoincrement, name varchar(128), info varchar(128)')
#     except:
#         print("{} created..")
#     sqlite.insert_value(table_name, '\"apple\",\"broccoli\"')
#     sqlite.select_data(table_name)
#     sqlite.update_data(table_name, 'name', "orange", 1)
#     sqlite.select_data(table_name)
#     sqlite.delete_data(table_name, 2)
#     sqlite.select_data(table_name)
