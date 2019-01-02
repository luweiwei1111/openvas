#coding=utf-8
import threading
import sqlite3
import sys
from sql.sqlite3_sql import Sql_django,Sql_topvas
from sql.mysql import MySql
import time

"""
说明：将Django里面的数据导出到表nvts_cn（mysql），用于中文显示

提前准备工作：
1.需要将django目录下的db.sqlite3库文件放在./db目录下
2.需要将topvas的tasks.db库文件放在./db目录下
3.需要将svn库里面的nvts_cn.sql导入到mysql数据库中

(备注：此处不处理tvid，需要张勇处理)
如何使用：在当前目录执行 python nvts_cn.py即可

数据导出：
导出mysql里面的nvts_cn数据
mysqldump  -uroot -p12345678 topvas nvts_cn > nvts_cn.sql
mysqldump  -uroot -p12345678 topvas nvts_ic_cn > nvts_ic_cn.sql
至此，数据转换完成，将nvts_cn.sql nvts_ic_cn.sql入svn库即可。
"""
class TS_Sync:
    def __init__(self):
        print('init')
        #nvts_cn --> nvts_cn_tmp
        #拷贝nvts_cn_tmp表结构用于创建表nvts_cn
        MySql.rename_nvts_cn()
        MySql.clear_nvts_cn()
        self.Tag_cn = ( 'summary',
                        'affected',
                        'solution',
                        'insight',
                        'vuldetect',
                        'impact',
                        'synopsis'
                        'description',
                        'exploitability_ease',
                        'risk_factor',
                        'metasploit_name',
                        'd2_elliot_name')

    def topvas_nvts_cn(self):
        #将topvas的tasks.db里面的nvts表数据插入到mysql数据库的nvts_cn表中
        progress = 0
        sr_nvts_list = Sql_topvas.select_nvts()
        for nvts_info in sr_nvts_list:
            id = nvts_info[0]
            uuid = nvts_info[1]
            oid = nvts_info[2] 
            version = nvts_info[3] 
            name = nvts_info[4] 
            comment = nvts_info[5] 
            copyright = nvts_info[6]
            cve = nvts_info[7] 
            bid = nvts_info[8] 
            xref = nvts_info[9] 
            tag = nvts_info[10]
            category = nvts_info[11]
            family = nvts_info[12] 
            cvss_base = nvts_info[13]
            creation_time = nvts_info[14]
            modification_time = nvts_info[15]
            solution_type = nvts_info[16]
            qod = nvts_info[17]
            qod_type = nvts_info[18]
            family_cn = ''
            #根据oid查找对应的中文信息
            nvts_cn_list = MySql.select_nvts_cn_tmp(oid)
            for nvts_cn_info in nvts_cn_list:
                name = nvts_cn_info[0]
                tag = nvts_cn_info[1]
                family_cn = nvts_cn_info[2]
            progress = progress + 1
            if progress%2000 == 0:
                print('INSERT progress:%d' %(progress))
            MySql.insert_nvts_cn(id, uuid, oid, version, name, comment, copyright, cve, bid, xref, tag, category, family, cvss_base, creation_time, modification_time, solution_type, qod, qod_type, family_cn)

    #更新family
    def update_family(self):
        #将family赋值给family_cn
        MySql.update_nvts_cn_family()

        #更新中文信息
        family_list = MySql.select_family_nvts_cn_tmp()
        for family_info in family_list:
            family = family_info[0]
            family_cn_list = MySql.select_family_cn_nvts_cn_tmp(family)
            family_cn = family
            for family_cn_info in family_cn_list:
                family_cn = family_cn_info[0]
            MySql.update_family_nvts_cn(family_cn, family)

    #更新其他中文信息
    #将blog_blogspost转到mysql的nvts_cn表中
    def django_nvts_cn_update(self):

        cn_info_results = Sql_django.select_blog_blogspost()
        count = 0
        for info_nvts in cn_info_results:
            count = count + 1
            nvts_oid = info_nvts[0]
            nvts_tag = info_nvts[1]
            summary_cn = info_nvts[2]
            affected_cn = info_nvts[3]
            solution_cn = info_nvts[4]
            insight_cn = info_nvts[5]
            vuldetect_cn = info_nvts[6]
            impact_cn = info_nvts[7]
            synopsis_cn = info_nvts[8]
            description_cn = info_nvts[9]
            exploitability_ease_cn = info_nvts[10]
            risk_factor_cn = info_nvts[11]
            metasploit_name_cn = info_nvts[12]
            d2_elliot_name_cn = info_nvts[13]
            name_cn = info_nvts[14]
            #family_cn = info_nvts[15]

            cn_nvts_tag = ''
            if nvts_tag != 'NOTAG':
                #解析tag
                tag_list = nvts_tag.split('|')
                tag_name_desc = ''
                for tag_info in tag_list:
                    tag_name = tag_info.split('=')[0]
                    if tag_name not in self.Tag_cn:
                        cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                    else:
                        if tag_name == 'summary':
                            if summary_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|summary=' + summary_cn
                        if tag_name == 'affected':
                            if affected_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|affected=' + affected_cn
                        if tag_name == 'solution':
                            if solution_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|solution=' + solution_cn
                        if tag_name == 'insight':
                            if insight_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|insight=' + insight_cn
                        if tag_name == 'vuldetect':
                            if vuldetect_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|vuldetect=' + vuldetect_cn
                        if tag_name == 'impact':
                            if impact_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|impact=' + impact_cn
                        if tag_name == 'synopsis':
                            if synopsis_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|synopsis=' + synopsis_cn
                        if tag_name == 'description':
                            if description_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|description=' + description_cn
                        if tag_name == 'exploitability_ease':
                            if exploitability_ease_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|exploitability_ease=' + exploitability_ease_cn
                        if tag_name == 'risk_factor':
                            if risk_factor_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|risk_factor=' + risk_factor_cn
                        if tag_name == 'metasploit_name':
                            if metasploit_name_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|metasploit_name=' + metasploit_name_cn
                        if tag_name == 'd2_elliot_name':
                            if d2_elliot_name_cn is None:
                                #未翻译
                                cn_nvts_tag = cn_nvts_tag + '|' + tag_info
                            else:
                                cn_nvts_tag = cn_nvts_tag + '|d2_elliot_name=' + d2_elliot_name_cn 
                if count%2000 == 0:
                    print('update progress->' + str(count))

                #print('#english tag:' + nvts_tag)
                #print('#chinese tag:' + cn_nvts_tag)

                cn_nvts_tag_sql = cn_nvts_tag[1:]
                MySql.update_nvts_cn_tag(cn_nvts_tag_sql, name_cn, nvts_oid)

        print('######update tag name_cn OK')

    #更新tvid
    def update_tvid(self):
        
        results = MySql.select_nvts_cn_fortvid()

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
            MySql.update_nvts_cn_tvid(tvid, oid)
            #cursor.execute("update nvts_cn set tvid='%s' where oid = '%s';" % (tvid, oid))

        print('update tvid ok')

    #删除多与数据
    def delete_data(self):
        #删除family为'Weak Passwords'、'Credentials'
        MySql.mysql_exec_commit("delete from nvts_cn where family in('Weak Passwords', 'Credentials')")
        #删除临时表nvts_cn_tmp
        MySql.mysql_exec_commit("delete from nvts_cn_tmp;")

    def data_to_dict(self, data, interval_kv, interval_dict):
        #将data转化为dict
        dict_tag = {}
        for item in data.split(interval_dict):
            list_item  = item.split(interval_kv)
            key = list_item[0]
            value = list_item[1]
            dict_tag[key] = value

        return dict_tag

    def init_ic_cn(self):
        #清空nvts_ic_cn表数据
        MySql.clear_nvts_ic_cn()
        nvts_cn_info = MySql.select_nvts_cn_all()
        count = 0
        for nvts_info in nvts_cn_info:
            id_id = nvts_info[0]
            uuid = nvts_info[1]
            oid = nvts_info[2]
            version = nvts_info[3]
            name = nvts_info[4]
            comment = nvts_info[5]
            copyright = nvts_info[6]
            cve = nvts_info[7]
            bid = nvts_info[8]
            xref = nvts_info[9] 
            tag = nvts_info[10]
            category = nvts_info[11]
            family = nvts_info[12]
            cvss_base = nvts_info[13]
            creation_time = nvts_info[14]
            modification_time = nvts_info[15]
            solution_type = nvts_info[16]
            qod = nvts_info[17] 
            qod_type = nvts_info[18]
            family_cn = nvts_info[19] 
            tvid = nvts_info[20]
            key_list = []
            dict_data = self.data_to_dict(tag, '=', '|')
            for key in dict_data:
                key_list.append(key)
            if 'vender' in key_list:
                count = count + 1
                print('ic_cn prgress:%d'%(count))
                vender_id = dict_data['vender']
                MySql.insert_nvts_ic_cn(id_id, uuid, oid, version, name, comment, copyright, cve, bid, xref, tag, category,family, vender_id, cvss_base, creation_time, modification_time, solution_type, qod, qod_type, family_cn, tvid)


if __name__ == '__main__':
    print('###1.INIT DB')
    ts_sync = TS_Sync()
    
    print('###2.INSERT INTO nvts_cn MYSQL DB (from sqlite3)')
    ts_sync.topvas_nvts_cn()
    
    print('###3.UPDATE family (CN)')
    ts_sync.update_family()
    
    print('###4.UPDATE tag & name (CN)')
    ts_sync.django_nvts_cn_update()
    
    print('###5.UPDATE tvid')
    ts_sync.update_tvid()

    print('###6.delete data')
    ts_sync.delete_data()

    print('###7.insert into nvts_ic_cn')
    ts_sync.init_ic_cn()

    print('###7.DATA Conversion Finish!!!')