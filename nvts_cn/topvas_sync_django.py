from sql.sqlite3_sql import Sql_topvas
from sql.sqlite3_sql import Sql_django

"""
准备工作：
1.库文件准备  db.sqlite3 tasks.db
"""

class SyncData:

    def __init__(self):
        print('##data init')
        Sql_django.sql_exec('alter table blog_blogspost rename to blog_blogspost_bak;')
        Sql_django.sql_exec('create table blog_blogspost as select * from blog_blogspost_bak where 0=1;')

    def sqliteEscape(self, keyWord):
        return keyWord.replace("/", "//").replace("'", "''").replace("[", "/[").replace("]", "/]").replace("%", "/%").replace("&","/&").replace("_", "/_").replace("(", "/(").replace(")", "/)")

    def sqliteReplace(self, keyWord):
        if keyWord == None:
            return ""
        return keyWord.replace('\'', '\'\'')

    def data_to_dict(self, data, interval_kv, interval_dict):
        #将data转化为dict
        dict_tag = {}
        for item in data.split(interval_dict):
            list_item  = item.split(interval_kv)
            key = list_item[0]
            value = list_item[1]
            dict_tag[key] = value

        return dict_tag

    def update_tag(self, result_tag):
        #更新tag数据
        count_set = 0
        for info in result_tag:
            oid = info[0]
            name = info[1].replace('\'', '\'\'')
            tag_data = info[2]
            summary = ''
            affected = ''
            solution = ''
            insight = ''
            vuldetect = ''
            impact = ''
            synopsis = ''
            description = ''
            exploitability_ease = ''
            risk_factor = ''
            metasploit_name = ''
            d2_elliot_name = ''

            if tag_data != 'NOTAG':
                key_list = []
                dict_data = self.data_to_dict(tag_data, '=', '|')
                for key in dict_data:
                    key_list.append(key)
                if 'summary' in key_list:
                    summary = dict_data['summary'].replace('\'', '\'\'')
                if 'affected' in key_list:
                    affected = dict_data['affected'].replace('\'', '\'\'')
                if 'solution' in key_list:
                    solution = dict_data['solution'].replace('\'', '\'\'')
                if 'insight' in key_list:
                    insight = dict_data['insight'].replace('\'', '\'\'')
                if 'vuldetect' in key_list:
                    vuldetect = dict_data['vuldetect'].replace('\'', '\'\'')
                if 'impact' in key_list:
                    impact = dict_data['impact'].replace('\'', '\'\'')
                if 'synopsis' in key_list:
                    synopsis = dict_data['synopsis'].replace('\'', '\'\'')
                if 'description' in key_list:
                    description = dict_data['description'].replace('\'', '\'\'')
                if 'exploitability_ease' in key_list:
                    exploitability_ease = dict_data['exploitability_ease'].replace('\'', '\'\'')
                if 'risk_factor' in key_list:
                    risk_factor = dict_data['risk_factor'].replace('\'', '\'\'')
                if 'metasploit_name' in key_list:
                    metasploit_name = dict_data['metasploit_name'].replace('\'', '\'\'')
                if 'd2_elliot_name' in key_list:
                    d2_elliot_name = dict_data['d2_elliot_name'].replace('\'', '\'\'')
            
            count_set = count_set + 1
            if count_set % 1000 == 0:
                print('##Update Progress##' + str(count_set))
            Sql_django.update_blog_blogspost(summary, affected, solution, insight, vuldetect, impact, synopsis, description, exploitability_ease, risk_factor, metasploit_name, d2_elliot_name, oid, name)

    #创建表 blog_blogspost 并插入数据
    def data_init(self):
        #插入数据nvts -> blog_blogspost
        attach_sql = """attach "db/tasks.db" as t1;"""
        Sql_django.sql_exec(attach_sql)
        Sql_django.sql_exec('insert into blog_blogspost(id, oid, name, name_cn, tag, family, family_cn) select id, oid, name, name, tag, family, family from t1.nvts order by id;')
        
        Sql_django.sql_exec("update blog_blogspost set is_change='0' where 1=1;")
        #创建索引oid、name
        Sql_django.sql_select_exec('create index idx_blog_blogspost_oid_name on blog_blogspost(oid, name);')

        #更新标签
        result_tag = Sql_django.sql_select_exec('select oid, name, tag from blog_blogspost order by id;')
        self.update_tag(result_tag)

    #更新中文信息
    def sync_cn_info(self):
        count = 0
        bak_cn_info = Sql_django.sql_select_exec("select oid, name, name_cn, family, family_cn,affected, affected_cn, summary, summary_cn, solution, solution_cn, insight, insight_cn, vuldetect, vuldetect_cn, impact, impact_cn, synopsis, synopsis_cn, description, description_cn, exploitability_ease, exploitability_ease_cn, risk_factor, risk_factor_cn, metasploit_name, metasploit_name_cn, d2_elliot_name, d2_elliot_name_cn, is_change from blog_blogspost_bak;")
        
        for cn_info in bak_cn_info:
            change_flag = False
            count = count + 1
            oid = cn_info[0]
            #待修改,需要根据tag来进行修改
            name = self.sqliteReplace(cn_info[1])
            name_cn = self.sqliteReplace(cn_info[2])
            family = self.sqliteReplace(cn_info[3])
            family_cn = ''
            #family_cn = self.sqliteReplace(cn_info[4])
            affected = self.sqliteReplace(cn_info[5])
            affected_cn = ''
            #affected_cn = self.sqliteReplace(cn_info[6])
            summary = self.sqliteReplace(cn_info[7])
            summary_cn = ''
            #summary_cn = self.sqliteReplace(cn_info[8])
            solution = self.sqliteReplace(cn_info[9])
            solution_cn = ''
            #solution_cn = self.sqliteReplace(cn_info[10])
            insight = self.sqliteReplace(cn_info[11])
            insight_cn = ''
            #insight_cn = self.sqliteReplace(cn_info[12])
            vuldetect = self.sqliteReplace(cn_info[13])
            vuldetect_cn = ''
            #vuldetect_cn = self.sqliteReplace(cn_info[14])
            impact = self.sqliteReplace(cn_info[15])
            impact_cn = ''
            #impact_cn = self.sqliteReplace(cn_info[16])
            synopsis = self.sqliteReplace(cn_info[17])
            synopsis_cn = ''
            #synopsis_cn = self.sqliteReplace(cn_info[18])
            description = self.sqliteReplace(cn_info[19])
            description_cn = ''
            #description_cn = self.sqliteReplace(cn_info[20])
            exploitability_ease = self.sqliteReplace(cn_info[21])
            exploitability_ease_cn = ''
            #exploitability_ease_cn = self.sqliteReplace(cn_info[22])
            risk_factor = self.sqliteReplace(cn_info[23])
            risk_factor_cn = ''
            #risk_factor_cn = self.sqliteReplace(cn_info[24])
            metasploit_name = self.sqliteReplace(cn_info[25])
            metasploit_name_cn = ''
            #metasploit_name_cn = self.sqliteReplace(cn_info[26])
            d2_elliot_name = self.sqliteReplace(cn_info[27])
            d2_elliot_name_cn = ''
            #d2_elliot_name_cn = self.sqliteReplace(cn_info[28])
            is_change = cn_info[29]
            #通过oid、name查找是否存在
            rets = Sql_django.sql_select_exec("SELECT EXISTS(SELECT 1 FROM blog_blogspost WHERE oid = '%s' and name = '%s');"%(oid, name))
            for info in rets:
                ret = info[0]
                #print('ret:%s'%(ret))

            if count % 1000 == 0:
                print('Progress:%d'%(count))
            if ret == 1:
                src_info_details = Sql_django.sql_select_exec("SELECT family, affected, summary, solution, insight, vuldetect, impact, synopsis, description, exploitability_ease, risk_factor, metasploit_name, d2_elliot_name  FROM blog_blogspost WHERE oid = '%s' and name = '%s';" % (oid, name))[0];
                #print(src_info_results)
                #src_info_details = src_info_results[0]
                #1.family
                family_src = src_info_details[0]
                if family_src != '' and family_src == family:
                    family_cn = self.sqliteReplace(cn_info[4])
                else:
                    family_cn = family
                
                #检查是否需要重新翻译
                if family_src != '' and family_src != family:
                    change_flag = True

                #2.affected 
                affected_src = src_info_details[1]
                if affected_src != '' and affected_src == affected:
                    affected_cn = self.sqliteReplace(cn_info[6])
                else:
                    affected_cn = affected
                
                #检查是否需要重新翻译
                if affected_src != '' and affected_src != affected:
                    change_flag = True

                #3.summary
                summary_src = src_info_details[2]
                if summary_src != '' and summary_src == summary:
                    summary_cn = self.sqliteReplace(cn_info[8])
                else:
                    summary_cn = summary
                
                #检查是否需要重新翻译
                if summary_src != '' and summary_src != summary:
                    change_flag = True

                #4.solution
                solution_src = src_info_details[3]
                if solution_src != '' and solution_src == solution:
                    solution_cn = self.sqliteReplace(cn_info[10])
                else:
                    solution_cn = solution
                
                #检查是否需要重新翻译
                if solution_src != '' and solution_src != solution:
                    change_flag = True

                #5.insight
                insight_src = src_info_details[4]
                if insight_src != '' and insight_src == insight:
                    insight_cn = self.sqliteReplace(cn_info[12])
                else:
                    insight_cn = insight
                
                #检查是否需要重新翻译
                if insight_src != '' and insight_src != insight:
                    change_flag = True

                #6.vuldetect
                vuldetect_src = src_info_details[5]
                if vuldetect_src != '' and vuldetect_src == vuldetect:
                    vuldetect_cn = self.sqliteReplace(cn_info[14])
                else:
                    vuldetect_cn = vuldetect
                
                #检查是否需要重新翻译
                if vuldetect_src != '' and vuldetect_src != vuldetect:
                    change_flag = True

                #7.impact
                impact_src = src_info_details[6]
                if impact_src != '' and impact_src == impact:
                    impact_cn = self.sqliteReplace(cn_info[16])
                else:
                    impact_cn = impact
                
                #检查是否需要重新翻译
                if impact_src != '' and impact_src != impact:
                    change_flag = True
                
                #8.synopsis
                synopsis_src = src_info_details[7]
                if synopsis_src != '' and synopsis_src == synopsis:
                    synopsis_cn = self.sqliteReplace(cn_info[18])
                else:
                    synopsis_cn = synopsis
                
                #检查是否需要重新翻译
                if synopsis_src != '' and synopsis_src != synopsis:
                    change_flag = True
                
                #9.description
                description_src = src_info_details[8]
                if description_src != '' and description_src == description:
                    description_cn = self.sqliteReplace(cn_info[20])
                else:
                    description_cn = description
                
                #检查是否需要重新翻译
                if description_src != '' and description_src != description:
                    change_flag = True

                #10.exploitability_ease
                exploitability_ease_src = src_info_details[9]
                if exploitability_ease_src != '' and exploitability_ease_src == exploitability_ease:
                    exploitability_ease_cn = self.sqliteReplace(cn_info[22])
                else:
                    exploitability_ease_cn = exploitability_ease
                
                #检查是否需要重新翻译
                if exploitability_ease_src != '' and exploitability_ease_src != exploitability_ease:
                    change_flag = True

                #11.risk_factor
                risk_factor_src = src_info_details[10]
                if risk_factor_src != '' and risk_factor_src == risk_factor:
                    risk_factor_cn = self.sqliteReplace(cn_info[24])
                else:
                    risk_factor_cn = risk_factor
                
                #检查是否需要重新翻译
                if risk_factor_src != '' and risk_factor_src != risk_factor:
                    change_flag = True

                #12.metasploit_name
                metasploit_name_src = src_info_details[11]
                if metasploit_name_src != '' and metasploit_name_src == metasploit_name:
                    metasploit_name_cn = self.sqliteReplace(cn_info[26])
                else:
                    metasploit_name_cn = metasploit_name
                
                #检查是否需要重新翻译
                if metasploit_name_src != '' and metasploit_name_src != metasploit_name:
                    change_flag = True

                #13.d2_elliot_name
                d2_elliot_name_src = src_info_details[12]
                if d2_elliot_name_src != '' and d2_elliot_name_src == d2_elliot_name:
                    d2_elliot_name_cn = self.sqliteReplace(cn_info[28])
                else:
                    d2_elliot_name_cn = d2_elliot_name
                
                #检查是否需要重新翻译
                if d2_elliot_name_src != '' and d2_elliot_name_src != d2_elliot_name:
                    change_flag = True

                if change_flag == True:
                    is_change = '0'
                else:
                    is_change = '1'
                Sql_django.update_cn_info(oid, name, name_cn, family_cn, affected_cn, summary_cn,solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, is_change)


if __name__ == '__main__':
    syncdata = SyncData()

    #插入nvts表中数据到blog_blogspost
    #更新tag、name_cn、family_cn
    print('update tag')
    syncdata.data_init()
    syncdata.sync_cn_info()
    Sql_django.sql_exec("drop table blog_blogspost_bak;")