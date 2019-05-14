# ftp服务端入口
from tkinter import *
from multiprocessing import Process
from server import *
from server_ui_top_menu import *
from server_ui_top_list import *
from server_ui_usr_list import *


class FtpServerUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('FTP服务器')
        # self.root.geometry('300x400')
    
    # 启动入口
    def run(self):
        self.create_component()
        self.root.mainloop()
    
    # 创建组件
    def create_component(self):
        # 菜单
        self.top_menu = MenuBar(self.root)
        # 文件列表
        self.dirlist = FileListBox(self.root)
        # 在线用户列表
        self.online_usr = UsrListBox(self.root)
        # 显示出来
        self.top_menu.show()
        self.dirlist.show()
        self.online_usr.show()

        # 为相关按钮或者菜单项绑定事件
        self.dirlist.display_file_list()
        self.online_usr.display_online_usr()

if __name__ == '__main__':
    FtpServerUI().run()
