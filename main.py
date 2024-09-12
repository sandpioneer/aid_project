from client_ui_main import *
from ftp_server_main import *
from multiprocessing import Process
from tkinter import *

class SuperFTP:
    def __init__(self):
        self.root = Tk()

    # 启动客户端
    def run_client(self):
        p = Process(target=FtpClientUI().run())
        p.daemon = True
        p.start()
    
    # 启动服务端
    def run_server(self):
        p = Process(target=FtpServerUI().run())
        p.daemon = True
        p.start()
    
    # 启动
    def run(self):
        self.root.title('超级管理器')
        self.labframe = LabelFrame(self.root, text='超级启动器！', padx=100, pady=30)

        self.btn_server = Button(self.labframe, text='SERVER NOW', command=self.run_server)
        self.btn_server.pack()

        self.btn_client = Button(self.labframe, text='CLIENT NOW', command=self.run_client)
        self.btn_client.pack(pady=15)

        self.labframe.pack(expand=YES, padx=100, pady=50)
        self.root.mainloop()


if __name__ == '__main__':
    SuperFTP().run()
