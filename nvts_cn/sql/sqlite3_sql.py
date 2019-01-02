import sqlite3

#for topvas DB
SQLITE3_DB = './db/tasks.db'
cnx_tp = sqlite3.connect(SQLITE3_DB, check_same_thread = False)
cur_tp = cnx_tp.cursor()

class Sql_topvas:
    
    @classmethod
    def select_nvts(cls):
        sql = 'select * from nvts;'

        print(sql)
        try:
            cur_tp.execute(sql)
        except:
            print('#select sql error:' + sql)
        return cur_tp.fetchall()

    @classmethod
    def sql_exec(cls, sql):

        print(sql)
        try:
            cur_tp.execute(sql)
        except:
            print('#ERROR#topvas exec sql error:%s'%(sql))
        cnx_tp.commit()

    @classmethod
    def sql_select_exec(cls, sql):

        #print(sql)
        try:
            cur_tp.execute(sql)
        except:
            print('#ERROR#topvas sql error:' + sql)
        return cur_tp.fetchall()

#for django DB
SQLITE3_DB = './db/db.sqlite3'
cnx_dj = sqlite3.connect(SQLITE3_DB, check_same_thread = False)
cur_dj = cnx_dj.cursor()

class Sql_django:

    @classmethod
    def select_blog_blogspost(cls):
        sql = 'select oid, tag, summary_cn, affected_cn, solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, name_cn from blog_blogspost;'

        print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#select sql error:' + sql)
        return cur_dj.fetchall()

    @classmethod
    def sql_exec(cls, sql):

        print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#django exec sql error:%s'%(sql))
        cnx_dj.commit()

    @classmethod
    def sql_select_exec(cls, sql):

        #print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#django sql error:' + sql)
        return cur_dj.fetchall()

    @classmethod
    def update_blog_blogspost(cls, summary, affected, solution, insight, vuldetect, impact, synopsis, description, exploitability_ease, risk_factor, metasploit_name, d2_elliot_name, oid, name):
        sql = """update blog_blogspost set  
            summary = \'%s\',
            affected = \'%s\',
            solution = \'%s\',
            insight = \'%s\',
            vuldetect = \'%s\',
            impact = \'%s\',
            synopsis = \'%s\',
            description = \'%s\',
            exploitability_ease = \'%s\',
            risk_factor = \'%s\',
            metasploit_name = \'%s\',
            d2_elliot_name = \'%s\'  
            where oid = \'%s\' and name = \'%s\';""" % (summary, affected, solution, insight, vuldetect, impact, synopsis, description, exploitability_ease, risk_factor, metasploit_name, d2_elliot_name, oid, name)

        #print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#update sql error:' + sql)
        cnx_dj.commit()

    @classmethod
    def update_cn_info(cls, oid, name, name_cn, family_cn, affected_cn, summary_cn,solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, is_change):
        sql = "update blog_blogspost set name_cn  = '%s', family_cn  = '%s', affected_cn = '%s', summary_cn = '%s',solution_cn = '%s', insight_cn = '%s', vuldetect_cn = '%s', impact_cn = '%s', synopsis_cn = '%s', description_cn = '%s', exploitability_ease_cn = '%s', risk_factor_cn = '%s', metasploit_name_cn = '%s', d2_elliot_name_cn = '%s', is_change = '%s' where oid = '%s' and name = '%s'" % (name_cn, family_cn, affected_cn, summary_cn,solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, is_change, oid, name)

        #print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#update sql error:' + sql)
        cnx_dj.commit()