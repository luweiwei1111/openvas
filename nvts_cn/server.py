import socketserver
import json

class Server(socketserver.BaseRequestHandler):
    def process_data(self, client_data):
        #处理client段的json数据
        return False

    def handle(self):  #父类方法，重写handle方法
        print('server端启动...')

        MAX_BUF_LEN = 1024*10
        inp = {
            "code": 0,
            "msg": "Process data OK"
        }

        conn=self.request   #等于conn,adress= server.accept()
        print(self.client_address)

        while True:
            client_data=conn.recv(MAX_BUF_LEN)
            print(str(client_data,'utf8'))

            process_flag = self.process_data(client_data)
            if process_flag == False:
                inp['code'] = 100
                inp['msg'] = "Process data Failed"
                json_inp = json.dumps(inp)
            
            conn.sendall(bytes(json_inp,'utf8'))
            break

        #断开连接
        print('close conn')
        conn.close()

if __name__=='__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1', 11000), Server)
    server.serve_forever()
