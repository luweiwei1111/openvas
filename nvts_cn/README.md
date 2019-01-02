1.准备库文件
db.sqlit3
tasks.db
nvts_cn.sql
nvts_ic_cn.sql
sql导入mysql数据库中（清空mysql topvas库里面的数据，再导入），sqlite3的库文件放在./db目录下

2.执行顺序
1) 将topvas的数据转到django： python topvas_sync_django.py
2) 将django里面的中文信息转回到topvas的nvts表中： python nvts_cn.py