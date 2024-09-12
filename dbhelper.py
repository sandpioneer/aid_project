import pymysql

class DBHelper:
    def __init__(self, dbname):
        self.conn = None
        self.host = '127.0.0.1'
        self.user = 'root'
        self.pwd = '123456'
        self.dbname = dbname
    
    # 连接数据库
    def open_conn(self):
        try:
            self.conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname)
        except Exception as e:
            print('数据库连接失败')
            print(e)
        # else:
        #     print('数据库连接成功！')
    
    # 关闭数据库
    def close_conn(self):
        try:
            self.conn.close()
        except Exception as e:
            print('数据库关闭失败')
            print(e)
        # else:
        #     print('数据库关闭成功！')
    
    # 查询
    def do_query(self, sql):
        try:
            # 获取游标
            cursor = self.conn.cursor()
            if not sql:
                print('SQL语句不合法！')
                return None
            # 执行查询
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print('查询失败！')
            print(e)
            return None
    
    # 增删改查
    def do_update(self, sql):
        try:
            cursor = self.conn.cursor()
            if not sql:
                print('SQL语句不合法！')
                return None
            # 执行查询
            result = cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return result
        except Exception as e:
            print('执行失败！')
            print(e)
            return None
        

# aid数据库操作
class AIDHelper:
    def __init__(self):
        self.dbname = 'aid'
        self.helper = DBHelper(self.dbname)
    
    # 基础查询用法
    def do_query(self, sql):
        self.helper.open_conn()
        result = self.helper.do_query(sql)
        self.helper.close_conn()
        return result
    
    # 增删改基础用法
    def do_update(self, sql):
        self.helper.open_conn()
        result = self.helper.do_update(sql)
        self.helper.close_conn()
        return result
    
    # 新用户注册
    def add_usr(self, username, userpwd):
        sql = "insert into usr values(0,'%s','%s')" % (username, userpwd)
        return self.do_update(sql)
    
    # 用户名是否存在
    def is_exist_username(self, username):
        sql = "select uid from usr where username = '%s'" % username
        return len(self.do_query(sql)) >= 1
    
    # 用户登录
    def usr_login(self, username, userpwd):
        sql = "select uid from usr where username = '%s' and userpwd = '%s'" % (username, userpwd)
        return len(self.do_query(sql)) >= 1
    
    # 用户上线
    def usr_online(self, username, ip):
        sql = "insert into usr_online values(0, '%s', '%s', now())" % (username, ip)
        return self.do_update(sql)
    
    # 用户是否在线
    def is_usr_online(self, username):
        sql = "select id from usr_online where username = '%s'" % username
        return len(self.do_query(sql)) >= 1

    # 用户离线
    def usr_offline(self, username):
        sql = "delete from usr_online where username = '%s'" % username
        return self.do_update(sql)
    
    # 获取在线用户列表
    def usr_online_list(self):
        sql = 'select * from usr_online'
        return self.do_query(sql)

if __name__ == '__main__':
    aid = AIDHelper()
    # sql = "insert into usr values(0,'admin','admin')"
    # print(aid.is_exist_username('1234')) 
    print(aid.usr_online('金毛狮王', '127.0.0.1')) 
    # print(aid.usr_login('admin', 'admin')) 
    # print(aid.usr_offline('123'))
    # print(aid.is_usr_online('admin'))


# 创建数据库
# create database aid default charset=utf8;

# 创建用户表
# create table usr(
#     uid int primary key auto_increment,
#     username varchar(128) unique,
#     userpwd varchar(128)
# )default charset=utf8;

# 创建用户在线表
# create table usr_online(
#     id int primary key auto_increment,
#     username varchar(128),
#     ip varchar(128),
#     time datetime
# )ENGINE=MEMORY default charset=utf8;