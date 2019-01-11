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
    def select_nvts_en(cls, oid):
        sql = "select id, name, family, tag from nvts where oid='%s';"%(oid)

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
    def update_blog_blogspost_cn(cls, summary_cn, affected_cn, solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, name_cn, family_cn, oid):
        sql = """update blog_blogspost set  
            summary_cn = \'%s\',
            affected_cn = \'%s\',
            solution_cn = \'%s\',
            insight_cn = \'%s\',
            vuldetect_cn = \'%s\',
            impact_cn = \'%s\',
            synopsis_cn = \'%s\',
            description_cn = \'%s\',
            exploitability_ease_cn = \'%s\',
            risk_factor_cn = \'%s\',
            metasploit_name_cn = \'%s\',
            d2_elliot_name_cn = \'%s\',
            name_cn = \'%s\',
            family_cn = \'%s\'
            where oid = \'%s\' ;""" % (summary_cn, affected_cn, solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, name_cn, family_cn, oid)

        print(sql)
        try:
            cur_dj.execute(sql)
            cnx_dj.commit()
            return True
        except:
            print('#ERROR#update sql error:' + sql)
            return False

        

    @classmethod
    def update_cn_info(cls, oid, name, name_cn, family_cn, affected_cn, summary_cn,solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, is_change):
        sql = "update blog_blogspost set name_cn  = '%s', family_cn  = '%s', affected_cn = '%s', summary_cn = '%s',solution_cn = '%s', insight_cn = '%s', vuldetect_cn = '%s', impact_cn = '%s', synopsis_cn = '%s', description_cn = '%s', exploitability_ease_cn = '%s', risk_factor_cn = '%s', metasploit_name_cn = '%s', d2_elliot_name_cn = '%s', is_change = '%s' where oid = '%s' and name = '%s'" % (name_cn, family_cn, affected_cn, summary_cn,solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, is_change, oid, name)

        #print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#update sql error:' + sql)
        cnx_dj.commit()

    @classmethod
    def select_exist_blog(cls, oid):
        sql = "SELECT EXISTS(SELECT 1 FROM blog_blogspost WHERE oid= '%s');"%(oid)
        print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#django sql error:' + sql)
        return cur_dj.fetchall()[0]

    @classmethod
    def select_blog_max_id(cls):
        sql = "select id from blog_blogspost order by id desc limit 1;"
        print(sql)
        try:
            cur_dj.execute(sql)
        except:
            print('#ERROR#django sql error:' + sql)
        return cur_dj.fetchall()[0]

    @classmethod
    def insert_blog_blogspost_cn(cls, id_id, oid, name, name_cn, tag, cn_ok, summary, summary_cn, affected, affected_cn, solution, solution_cn, insight, insight_cn, vuldetect, vuldetect_cn, impact, impact_cn, synopsis, synopsis_cn, description, description_cn, exploitability_ease, exploitability_ease_cn, risk_factor, risk_factor_cn, metasploit_name, metasploit_name_cn, d2_elliot_name, d2_elliot_name_cn, family, family_cn, is_change):
        sql = "insert into blog_blogspost(id, oid, name, name_cn, tag, cn_ok, summary, summary_cn, affected, affected_cn, solution, solution_cn, insight, insight_cn, vuldetect, vuldetect_cn, impact, impact_cn, synopsis, synopsis_cn, description, description_cn, exploitability_ease, exploitability_ease_cn, risk_factor, risk_factor_cn, metasploit_name, metasploit_name_cn, d2_elliot_name, d2_elliot_name_cn, family, family_cn, is_change) VALUES('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(id_id, oid, name, name_cn, tag, cn_ok, summary, summary_cn, affected, affected_cn, solution, solution_cn, insight, insight_cn, vuldetect, vuldetect_cn, impact, impact_cn, synopsis, synopsis_cn, description, description_cn, exploitability_ease, exploitability_ease_cn, risk_factor, risk_factor_cn, metasploit_name, metasploit_name_cn, d2_elliot_name, d2_elliot_name_cn, family, family_cn, is_change)
        
        print(sql)
        try:
            cur_dj.execute(sql)
            cnx_dj.commit()
            return True
        except:
            print('#ERROR#update sql error:' + sql)
            return False
        