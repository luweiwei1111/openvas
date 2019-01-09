from sql.sqlite3_sql import Sql_topvas
from sql.mysql import MySql
import json
import socket

class WebUI:
    def __init__(self, oid):
        
        self.oid = oid
        id_nvt = 0
        name = ''
        family = ''
        tag = ''
        #需要翻译的标签tag
        self.tag_g = [
            'summary', 'affected', 'solution', 'insight', 'vuldetect', 
            'impact', 'synopsis', 'description', 'exploitability_ease', 'risk_factor',
            'metasploit_name', 'd2_elliot_name'
            ]
        
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

        print('#######################################################')
        #根据oid获取英文信息
        nvts_en_infos_results = Sql_topvas.select_nvts_en(self.oid)
        if nvts_en_infos_results:
            id_nvt = int(nvts_en_infos_results[0][0])
            name = nvts_en_infos_results[0][1]
            family = nvts_en_infos_results[0][2]
            tag = nvts_en_infos_results[0][3]
            dict_data_tag = self.data_to_dict(tag, '=', '|')
            for key_tag in dict_data_tag:
                if key_tag in self.tag_g:
                    if key_tag == "summary":
                        summary = dict_data_tag[key_tag]
                    elif key_tag == "affected":
                        affected = dict_data_tag[key_tag]
                    elif key_tag == "solution":
                        solution = dict_data_tag[key_tag]
                    elif key_tag == "insight":
                        insight = dict_data_tag[key_tag]
                    elif key_tag == "vuldetect":
                        vuldetect = dict_data_tag[key_tag]
                    elif key_tag == "impact":
                        impact = dict_data_tag[key_tag]
                    elif key_tag == "synopsis":
                        synopsis = dict_data_tag[key_tag]
                    elif key_tag == "description":
                        description = dict_data_tag[key_tag]
                    elif key_tag == "exploitability_ease":
                        exploitability_ease = dict_data_tag[key_tag]
                    elif key_tag == "risk_factor":
                        risk_factor = dict_data_tag[key_tag]
                    elif key_tag == "metasploit_name":
                        metasploit_name = dict_data_tag[key_tag]
                    elif key_tag == "d2_elliot_name":
                        d2_elliot_name = dict_data_tag[key_tag]

        #根据oid获取英文信息，先初始化为英文信息
        name_cn = name
        family_cn = family
        summary_cn = summary
        affected_cn = affected
        solution_cn = solution
        insight_cn = insight
        vuldetect_cn = vuldetect
        impact_cn = impact
        synopsis_cn = synopsis
        description_cn = description
        exploitability_ease_cn = exploitability_ease
        risk_factor_cn = risk_factor
        metasploit_name_cn = metasploit_name
        d2_elliot_name_cn = d2_elliot_name

        nvts_cn_results = MySql.select_nvts_cn_infos(self.oid)
        if nvts_cn_results:
            name_cn = nvts_cn_results[0][0]
            family_cn = nvts_cn_results[0][1]
            tag_cn = nvts_cn_results[0][2]
            dict_data_tag = self.data_to_dict(tag_cn, '=', '|')
            for key_tag in dict_data_tag:
                if key_tag in self.tag_g:
                    if key_tag == "summary":
                        summary_cn = dict_data_tag[key_tag]
                        print('summary_cn:%s'%(summary_cn))
                    elif key_tag == "affected":
                        affected_cn = dict_data_tag[key_tag]
                        print('affected_cn:%s'%(affected_cn))
                    elif key_tag == "solution":
                        solution_cn = dict_data_tag[key_tag]
                        print('solution_cn:%s'%(solution_cn))
                    elif key_tag == "insight":
                        insight_cn = dict_data_tag[key_tag]
                        print('insight_cn:%s'%(insight_cn))
                    elif key_tag == "vuldetect":
                        vuldetect_cn = dict_data_tag[key_tag]
                        print('vuldetect_cn:%s'%(vuldetect_cn))
                    elif key_tag == "impact":
                        impact_cn = dict_data_tag[key_tag]
                        print('impact_cn:%s'%(impact_cn))
                    elif key_tag == "synopsis":
                        synopsis_cn = dict_data_tag[key_tag]
                        print('synopsis_cn:%s'%(synopsis_cn))
                    elif key_tag == "description":
                        description_cn = dict_data_tag[key_tag]
                        print('description_cn:%s'%(description_cn))
                    elif key_tag == "exploitability_ease":
                        exploitability_ease_cn = dict_data_tag[key_tag]
                        print('exploitability_ease_cn:%s'%(exploitability_ease_cn))
                    elif key_tag == "risk_factor":
                        risk_factor_cn = dict_data_tag[key_tag]
                        print('risk_factor_cn:%s'%(risk_factor_cn))
                    elif key_tag == "metasploit_name":
                        metasploit_name_cn = dict_data_tag[key_tag]
                        print('metasploit_name_cn:%s'%(metasploit_name_cn))
                    elif key_tag == "d2_elliot_name":
                        d2_elliot_name_cn = dict_data_tag[key_tag]
                        print('d2_elliot_name_cn:%s'%(d2_elliot_name_cn))

        print('#######################################################')
        #构造json串
        self.nvts_cn_json = {
            "id" : id_nvt,
            "oid": oid,
            "name": name,
            "name_cn": "",
            "tag": tag,
            "cn_ok": "0",
            "summary": summary,
            "summary_cn": summary_cn,
            "affected": affected,
            "affected_cn": affected_cn,
            "solution": solution,
            "solution_cn": solution_cn,
            "insight": insight,
            "insight_cn": insight_cn,
            "vuldetect": vuldetect,
            "vuldetect_cn": vuldetect_cn,
            "impact": impact,
            "impact_cn": impact_cn,
            "synopsis": synopsis,
            "synopsis_cn": synopsis_cn,
            "description": description,
            "description_cn": description_cn,
            "exploitability_ease": exploitability_ease,
            "exploitability_ease_cn": exploitability_ease_cn,
            "risk_factor": risk_factor,
            "risk_factor_cn": risk_factor_cn,
            "metasploit_name": metasploit_name,
            "metasploit_name_cn": metasploit_name_cn,
            "d2_elliot_name": d2_elliot_name,
            "d2_elliot_name_cn": d2_elliot_name_cn,
            "family": family,
            "family_cn": family_cn,
            "is_change": "0",
            }

    def data_to_dict(self, data, interval_kv, interval_dict):
        #将data转化为dict
        dict_tag = {}
        for item in data.split(interval_dict):
            list_item  = item.split(interval_kv)
            key = list_item[0]
            value = list_item[1]
            dict_tag[key] = value

        return dict_tag

    def load_json_nvst_cn(self):
        return json.dumps(self.nvts_cn_json)

def main():
    oid = "1.3.6.1.4.1.25623.1.0.901110"
    webui = WebUI(oid)
    json_str = webui.load_json_nvst_cn()
    print(json_str)

    #开始连接
    client=socket.socket()
    adress=('127.0.0.1', 11000)
    client.connect(adress)

    while True:
        client.sendall(bytes(json_str,'utf8'))
        #byte转为utf8字符串型
        res_data = client.recv(1024).decode('utf8')
        res_data = json.loads(res_data)
        if res_data['code'] == 0:
            print('data process success!!!')
        else:
            print('data process failed!!!')
        
        break

    client.close()

if __name__ == '__main__':
	main()