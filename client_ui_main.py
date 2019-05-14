from tkinter import *
from tkinter.messagebox import *
from threading import Thread
from client_ui_top_menu import *
from client_ui_top_file_list import * 
from client_ui_top_down_file_list import *
from login_ui import *
from reg_ui import *


class FtpClientUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('FTP客户端')
        self.root.resizable(width=False, height=False)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        # 菜单，文件，用户
        self.menubar = MenuBar(self.root)
        self.downbox = DownFileListBox(self.root)
        self.filebox = FileListBox(self.root, self.downbox)
    
    # 主要组件
    def primary_component(self):
        self.menubar.show()
        self.filebox.show()
        self.downbox.show()
        # 获取服务端文件列表
        self.filebox.display_file_list()
        # 更新已下载文件列表
        self.downbox.display_file_list()

    # 登录组件
    def login_component(self):
        self.login_ui = LoginModule(self.root)
        self.login_ui.create_component()
        self.login_ui.show()
        self.login_ui.btnlogin.bind('<Button-1>', self.click_login)
        self.login_ui.btnreg.bind('<Button-1>', self.click_reg)

    # 登录按钮
    def click_login(self, *args):
        labeluname = self.login_ui.labeluname
        labelupwd= self.login_ui.labelupwd
        usrname = self.login_ui.entryuname.get()
        usrpwd = self.login_ui.entryunpwd.get()
        if not usrname:
            labeluname.config({
                'fg':'red'
            })
            return
        else:
            labeluname.config({
                'fg':'black'
            })
        if not usrpwd:
            labelupwd.config({
                'fg':'red'
            })
            return
        else:
            labelupwd.config({
                'fg':'black'
            })
        cmd = LOGIN + ' %s %s' % (usrname, usrpwd)
        if FtpClient().run(cmd):
            self.menubar.user = usrname
            self.user = usrname
            self.primary_component()
            self.login_ui.discard()
        else:
            labeluname.config({
                'fg':'red'
            })
            labelupwd.config({
                'fg':'red'
            })

    # 注册按钮事件
    def click_reg(self, *args):
        self.login_ui.hide()
        self.reg_ui = RegModule(self.root)
        self.reg_ui.create_component()
        self.reg_ui.show()
        self.reg_ui.btnok.bind('<Button-1>', self.ensure_reg)

    # 注册
    def ensure_reg(self, *agrs):
        client = FtpClient()

        luname = self.reg_ui.labeluname
        lupwd = self.reg_ui.labelupwd
        lconfirm = self.reg_ui.labelconfirm
        uname = self.reg_ui.entryuname
        upwd = self.reg_ui.entryunpwd
        confirm = self.reg_ui.entryconfirm

        # 用户名不能为空
        if not uname.get():
            luname.config({
                'fg': 'red'
            })
            return
        else:
            luname.config({
                'fg': 'black'
            })
        # 密码不能为空
        if not upwd.get():
            lupwd.config({
                'fg': 'red'
            })
            return
        else:
            lupwd.config({
                'fg': 'black'
            })
        # 重复密码
        if not confirm.get():
            lconfirm.config({
                'fg': 'red'
            })
            return
        else:
            lconfirm.config({
                'fg': 'black'
            })
        # 两次输入是否一致
        if upwd.get() != confirm.get():
            lconfirm.config({
                'bg': 'red'
            })
            return
        # 输入符合要求，允许注册
        res = client.run(REG + ' %s %s' % (uname.get(), upwd.get()))
        if res:
            # 设置上线
            client.run(LOGIN + ' %s %s' % (uname.get(), upwd.get()))
            # 跳转至主界面
            self.primary_component()
            # 当前登录用户
            self.user = uname.get()
            self.menubar.user = uname.get()
            # 销毁注册界面
            self.reg_ui.discard()
        else:
            # 注册失败
            luname.config({
                'fg': 'red'
            })

    # 窗口关闭
    def close(self):
        # yes = askokcancel('是否退出？', '是否退出？')
        # if yes:
        client = FtpClient()
        if not hasattr(self, 'user'):
            self.user = 'admin'
        client.run(LOGOUT + ' %s' % self.user)
        self.root.destroy()

    # 启动
    def run(self):
        self.login_component()
        self.root.mainloop()

if __name__ == '__main__':
    FtpClientUI().run()