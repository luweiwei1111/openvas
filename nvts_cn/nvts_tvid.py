#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time


# 打开数据库连接
db = MySQLdb.connect("127.0.0.1", "root", "topsec*talent", "topvas", charset='utf8' )

cursor = db.cursor()
cursor.execute("SELECT oid, creation_time, family, category from nvts_cn;")
results = cursor.fetchall()

for item in results:
    oid = item[0]
    creation_time = int(item[1])
    family = item[2]
    category = int(item[3])
    
    timeArray = time.localtime(creation_time)
    year = time.strftime("%Y", timeArray)
    month = time.strftime("%m", timeArray)

    oid_split = oid.split(".")
    id = oid_split[len(oid_split)-1]
    
    tvid = "TVID-%s%s-%s" %(year, month, id)
    cursor.execute("update nvts_cn set tvid='%s' where oid = '%s';" % (tvid, oid))
    
db.commit()
db.close()

