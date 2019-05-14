# server2.py

from socket import *
from select import select
import os, sys, time
from multiprocessing import Value
from settings import *
from dbhelper import AIDHelper

ADDR = ('127.0.0.1', 10086)

# FTP服务器
class FtpServer:
    def __init__(self):
        self.db = AIDHelper()
        self.create_socket()
        self.bind_addr()
    
    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    # 绑定地址
    def bind_addr(self):
        self.sockfd.bind(ADDR)
        
    # 启动服务
    def run_forever(self):
        # 监听
        self.sockfd.listen(5)
        rlist, wlist, xlist = [self.sockfd], [], [] 
        # 开始监控
        while True:
            rs, ws, xs = select(rlist, wlist, xlist)
            for r in rs:
                if r is self.sockfd:
                    connfd, addr = r.accept()
                    print('connect from:', addr)
                    rlist.append(connfd)
                else:
                    try:
                        data = r.recv(MAX_TRANSFER_BLOCK).decode()
                    except Exception as e:
                        print('客户端中断...', e)
                        r.close()
                        rlist.remove(r)
                        continue
                    # 接收到空
                    if not data:
                        r.close()
                        rlist.remove(r)
                        continue
                    try:
                        # 处理请求
                        self.handle(data, r)
                    except Exception as e:
                        r.close()
                        rlist.remove(r)
                        print('请求处理错误！', e)
                        continue
    
    # 处理请求
    def handle(self, data, connfd):
        # 分析数据
        data = data.split(CMD_SPLIT)
        print(connfd.getpeername(), ':', data)
        cmd = data[0].upper()
        # 登录请求
        if cmd == LOGIN:
            self.do_login(data, connfd)
        elif cmd == LOGOUT:
            self.do_logout(data, connfd)
        # 注册请求
        elif cmd == REG:
            self.do_reg(data, connfd)
        elif cmd == LIST:
            self.do_list(data, connfd)
        # 下载请求
        elif cmd == DOWN:
            self.do_download(data, connfd)
        # 上传请求
        elif cmd == UPLOAD:
            self.do_upload(data, connfd)
        # 未识别的请求
        else:
            self.do_ignore(data, connfd)

    # 登录请求
    def do_login(self, cmd, connfd):
        username = cmd[1]
        pwd = cmd[2]
        res = self.db.usr_login(username, pwd)
        if res:
            resp = SUCCESS + CMD_SPLIT
            # 用户上线
            if not self.db.is_usr_online(username):
                self.db.usr_online(username, connfd.getpeername()[0])
        else:
            resp = FAILED + CMD_SPLIT + '用户账号，密码错误！'
        connfd.send(resp.encode())
    
    # 登出请求
    def do_logout(self, cmd, connfd):
        username = cmd[1]
        self.db.usr_offline(username)

    # 注册请求
    def do_reg(self, cmd, connfd):
        username = cmd[1]
        userpwd = cmd[2]
        # 加入数据库
        res = self.db.add_usr(username, userpwd)
        if res:
            resp = CMD_SPLIT.join([SUCCESS, username, userpwd])
        else:
            resp = FAILED
        connfd.send(resp.encode())

    # 获取文件列表
    def do_list(self, cmd, connfd):
        try:
            if len(cmd) == 1:
                # 获取根目录下文件列表
                dirs = os.listdir(PUBLIC_DIR)
            else:
                # 获取制定目录下文件
                dirs = os.listdir(PUBLIC_DIR + cmd[1])
            status = SUCCESS
        except Exception as e:
            print('【指定目录不存在】', e)
            connfd.send(FAILED.encode())
            return
        resp = status + CMD_SPLIT + CMD_SPLIT.join(dirs)
        connfd.send(resp.encode())

    # 下载请求
    def do_download(self, cmd, connfd):
        filename = cmd[1]
        # 打开文件
        try:
            f = open(PUBLIC_DIR + filename, 'rb')
        except Exception as e:
            print('文件出错了！', e)
            # 发送不能下载命令
            connfd.send(FAILED.encode())
            return
        
        # 发送可以下载命令
        filesize = os.path.getsize(PUBLIC_DIR + filename)
        connfd.send(CMD_SPLIT.join([SUCCESS, filename, str(filesize)]).encode())

        # 开始发送
        while True:
            time.sleep(SLEEP_TIME)
            data = f.read(MAX_TRANSFER_BLOCK)
            # 发送结束
            if not data:
                connfd.send(FILE_END_TAG.encode())
                print('[ %s ]发送完毕！' % filename)
                break
            # 正常发送
            connfd.send(data)
        
        # 发送完成，关闭文件
        f.close()

    # 上传处理
    def do_upload(self, cmd, connfd):
        filename = cmd[1]
        # 文件已存在
        if os.path.exists(PUBLIC_DIR + filename):
            connfd.send(FAILED.encode())
            return
        # 允许上传
        # 通知客户端
        resp = SUCCESS + CMD_SPLIT + filename
        connfd.send(resp.encode())
        # 接收文件大小等信息
        msg = connfd.recv(MAX_TRANSFER_BLOCK).decode().split(CMD_SPLIT)
        if msg[0] == FAILED:
            print('客户端不再上传了！')
            return
        # 获取文件大小
        filesize = int(msg[2])
        # 空文件不接受上传
        if filesize <= 0:
            print('空文件..')
            return
        # 开始接收
        bs = b''
        while True:
            try:
                data = connfd.recv(MAX_TRANSFER_BLOCK)
                if data.decode() == FILE_END_TAG:
                    print('[%s]接收完毕！'% filename)
                    break
            except Exception:
                print('已接受 %d 字节'%len(bs), time.ctime())
            
            bs += data
        
        # 保存
        try:
            with open(PUBLIC_DIR + filename, 'wb') as f:
                f.write(bs)
        except Exception as e:
            print('文件保存失败！', e)


    # 未识别请求
    def do_ignore(self, data, connfd):
        msg = 'IGNORE ' + '未识别的请求：' + str(data)
        connfd.send(msg.encode())

if __name__ == '__main__':
    ftp = FtpServer()
    print('server running...')
    ftp.run_forever()