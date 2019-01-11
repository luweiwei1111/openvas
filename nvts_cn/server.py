import socketserver
import logging
import json
from sql.sqlite3_sql import Sql_django

##################user config ##################
logger = logging.getLogger("django_server")
#############################################

def InitLog():
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("django_server.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

class Server(socketserver.BaseRequestHandler):

    def sqliteEscape(cls, keyWord):
        return keyWord.replace("'", "''")

    def process_data(self, client_data):
        #处理client段的json数据
        try:
            nvts_data = json.loads(client_data)
        except:
            #接收字符串非json，返回错误信息
            return 'data error'

        id_id = 0
        try:
            oid = nvts_data['oid']
        except:
            #接收字符串json中没有oid，返回错误信息
            return 'data error'

        name = self.sqliteEscape(nvts_data['name'])
        name_cn = self.sqliteEscape(nvts_data['name_cn'])
        tag = self.sqliteEscape(nvts_data['tag'])
        cn_ok = self.sqliteEscape(nvts_data['cn_ok'])
        summary = self.sqliteEscape(nvts_data['summary'])
        summary_cn = self.sqliteEscape(nvts_data['summary_cn'])
        affected = self.sqliteEscape(nvts_data['affected'])
        affected_cn = self.sqliteEscape(nvts_data['affected_cn'])
        solution = self.sqliteEscape(nvts_data['solution'])
        solution_cn = self.sqliteEscape(nvts_data['solution_cn'])
        insight = self.sqliteEscape(nvts_data['insight'])
        insight_cn = self.sqliteEscape(nvts_data['insight_cn'])
        vuldetect = self.sqliteEscape(nvts_data['vuldetect'])
        vuldetect_cn = self.sqliteEscape(nvts_data['vuldetect_cn'])
        impact = self.sqliteEscape(nvts_data['impact'])
        impact_cn = self.sqliteEscape(nvts_data['impact_cn'])
        synopsis = self.sqliteEscape(nvts_data['synopsis'])
        synopsis_cn = self.sqliteEscape(nvts_data['synopsis_cn'])
        description = self.sqliteEscape(nvts_data['description'])
        description_cn = self.sqliteEscape(nvts_data['description_cn'])
        exploitability_ease = self.sqliteEscape(nvts_data['exploitability_ease'])
        exploitability_ease_cn = self.sqliteEscape(nvts_data['exploitability_ease_cn'])
        risk_factor = self.sqliteEscape(nvts_data['risk_factor'])
        risk_factor_cn = self.sqliteEscape(nvts_data['risk_factor_cn'])
        metasploit_name = self.sqliteEscape(nvts_data['metasploit_name'])
        metasploit_name_cn = self.sqliteEscape(nvts_data['metasploit_name_cn'])
        d2_elliot_name = self.sqliteEscape(nvts_data['d2_elliot_name'])
        d2_elliot_name_cn = self.sqliteEscape(nvts_data['d2_elliot_name_cn'])
        family = self.sqliteEscape(nvts_data['family'])
        family_cn = self.sqliteEscape(nvts_data['family_cn'])
        is_change = '0'
        #根据oid查找是否存在
        exist_ret = Sql_django.select_exist_blog(oid)
        ret = exist_ret[0]
        logger.debug('recv hanle->ret:%d, oid:%s'%(ret, oid))

        if ret == 1:
            #存在则更新中文信息 
            #根据oid修改对应的中文信息
            logger.debug('update blog_blogspost cn info[%s]'%(oid))
            update_ret = Sql_django.update_blog_blogspost_cn(summary_cn, affected_cn, solution_cn, insight_cn, vuldetect_cn, impact_cn, synopsis_cn, description_cn, exploitability_ease_cn, risk_factor_cn, metasploit_name_cn, d2_elliot_name_cn, name_cn, family_cn, oid)
        else:
            #不存在则插入相关信息
            #取当前id的最大值加1
            id_ret = Sql_django.select_blog_max_id()
            #print('id_ret:%d'%(id_ret))
            #print(type(id_ret))
            id_id = id_ret[0] + 1
            logger.debug('insert blog_blogspost cn info[%s]'%(oid))
            update_ret = Sql_django.insert_blog_blogspost_cn(id_id, oid, name, name_cn, tag, cn_ok, summary, summary_cn, affected, affected_cn, solution, solution_cn, insight, insight_cn, vuldetect, vuldetect_cn, impact, impact_cn, synopsis, synopsis_cn, description, description_cn, exploitability_ease, exploitability_ease_cn, risk_factor, risk_factor_cn, metasploit_name, metasploit_name_cn, d2_elliot_name, d2_elliot_name_cn, family, family_cn, is_change)
        
        if update_ret == True:
            return 'success'
        else:
            return 'failed'

    def handle(self):  #父类方法，重写handle方法
        logger.debug('server端启动...')

        MAX_BUF_LEN = 1024*10
        inp = {
            "code": 0,
            "msg": "Process data OK"
        }

        conn=self.request   #等于conn,adress= server.accept()
        ip_address, port = self.client_address
        logger.debug('recv request:IP[%s] Port[%d]'%(ip_address, port))

        while True:
            try:
                client_data=conn.recv(MAX_BUF_LEN)
            except:
                logger.error('recv data failed')
                break
            #print(str(client_data,'utf8'))

            process_msg = self.process_data(client_data)

            if process_msg == 'failed':
                inp['code'] = 100
                inp['msg'] = "Process data Failed"
            elif process_msg == 'data error':
                inp['code'] = 101
                inp['msg'] = "Recv data format error"
                logger.error('recv data format error,break')
                break
            else:
                inp['code'] = 0
                inp['msg'] = "Process data OK"

            json_inp = json.dumps(inp)
            conn.sendall(bytes(json_inp,'utf8'))
            break

        #断开连接
        logger.debug('close conn')
        conn.close()

if __name__=='__main__':
    InitLog()
    server=socketserver.ThreadingTCPServer(('0.0.0.0', 11000), Server)
    server.serve_forever()
