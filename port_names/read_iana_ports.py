# -*- coding: utf-8 -*-
from xml.dom.minidom import parse # 导入模块
import sqlite3

#for topvas DB
SQLITE3_DB = 'port_names.db'
db = sqlite3.connect(SQLITE3_DB, check_same_thread = False)
cursor = db.cursor()

class Sql:
    @classmethod
    def sql_exec(cls, sql):
        #print(sql)
        try:
            cursor.execute(sql)
        except:
            print('#ERROR#topvas exec sql error:%s'%(sql))
        db.commit()

    @classmethod
    def sql_select_exec(cls, sql):
        print(sql)
        try:
            cursor.execute(sql)
        except:
            print('#ERROR#topvas sql error:' + sql)
        return cursor.fetchall()

    @classmethod
    def sql_close_db(cls):
        print('close sqlite db')
        db.close()

def main_port_names():
    #创建数据库表port_names
    sql_ctl = "CREATE TABLE IF NOT exists port_names (id INTEGER PRIMARY KEY, number INTEGER, protocol, name,  UNIQUE (number, protocol) ON CONFLICT REPLACE);"
    Sql.sql_exec(sql_ctl)

    #解析xml并入库
    domTree = parse("service-names-port-numbers.xml") # 使用minidom解析器打开 XML 文档
    root = domTree.documentElement # 获取文档元素
    ps = root.getElementsByTagName("record") # 获取集合中的 record 元素
    x_id = 0
    for p in ps: # 输出所有的值
        #print('#######################################')
        try:
            x_name = p.getElementsByTagName("name")[0].childNodes[0].data
        except:
            continue

        try:
            x_number = p.getElementsByTagName("number")[0].childNodes[0].data
            if '-' in x_number:
                continue
        except:
            continue

        try:
            x_protocol = p.getElementsByTagName("protocol")[0].childNodes[0].data
        except:
            continue
        
        x_id = x_id + 1

        insert_sql = "insert into port_names(id, number, protocol, name) values(%d, '%s', '%s', '%s')" %(x_id, x_number, x_protocol, x_name)
        Sql.sql_exec(insert_sql)

    Sql.sql_close_db()

if __name__ == '__main__':
    main_port_names()