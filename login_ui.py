from tkinter import *
from client import *
from settings import *
from tkinter.messagebox import showinfo, showwarning


class LoginModule:
    # 此模块负责处理登陆
    def __init__(self, master):
        self.master = master
        self.frame = LabelFrame(self.master, text='用户登录', padx=60, pady=30)
    
    # 创建控件
    def create_component(self):
        self.labeluname = Label(self.frame, text='用户名', anchor='nw')
        self.labelupwd = Label(self.frame, text='密码', anchor='nw')
        self.entryuname = Entry(self.frame)
        self.entryunpwd = Entry(self.frame, show='*')
        
        self.labeluname.pack(fill=X)
        self.entryuname.pack()
        self.labelupwd.pack(fill=X)
        self.entryunpwd.pack()

        # 登录按钮
        self.btnlogin = Button(self.frame, text='登录', padx=2)
        self.btnlogin.pack(side=LEFT, padx=12, pady=8)

        # 注册按钮
        self.btnreg = Button(self.frame, text='注册', padx=2)
        self.btnreg.pack(side=LEFT, padx=8)

    # 登录
    def do_login(self):
        usrname = self.entryuname.get()
        usrpwd = self.entryunpwd.get()
        if not usrname:
            self.labeluname.config({
                'fg':'red'
            })
            return
        else:
            self.labeluname.config({
                'fg':'black'
            })
        if not usrpwd:
            self.labelupwd.config({
                'fg':'red'
            })
            return
        else:
            self.labelupwd.config({
                'fg':'black'
            })
        cmd = LOGIN + ' %s %s' % (usrname, usrpwd)
        if FtpClient().run(cmd):
            showinfo('登录成功！', '登录成功！')
        else:
            showwarning('登录失败！', '登录失败！')

    # 显示
    def show(self):
        self.frame.pack(expand=YES, padx=100, pady=60)

    # 隐藏
    def hide(self):
        self.frame.pack_forget()

    # 销毁
    def discard(self):
        self.frame.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title('登录')
    l = LoginModule(root)
    l.create_component()
    l.show()
    l.master.mainloop()    