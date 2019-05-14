from tkinter import *
from tkinter.messagebox import showinfo, showerror, askokcancel
from client import *
from multiprocessing import Process

class MenuBar:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.menubar = Menu(master)

    # 将菜单显示出来
    def show(self):
        # 文件菜单
        self.filemenu = Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label='测试连接', command=self.connect_server)
        # filemenu.add_command(label='保存')
        self.filemenu.add_command(label='退出', command=self.close)
        self.menubar.add_cascade(label='开始(S)', menu=self.filemenu)

        # 更多
        self.othermenu = Menu(self.menubar, tearoff=False)
        self.othermenu.add_command(label='开心一下')
        self.othermenu.add_command(label='关于', command=self.about)
        self.menubar.add_cascade(label='更多(M)', menu=self.othermenu)

        # 添加至顶层
        self.master.config(menu=self.menubar)
    
    # 隐藏
    def hide(self):
        self.menubar.pack_forget()
    
    # 彻底销毁
    def discard(self):
        self.menubar.destroy()

    # 连接服务选项
    def connect_server(self):
        res = FtpClient().run(LOGIN + " %s %s" % (TEST_CONNECT_USR, TEST_CONNECT_USRPWD))
        if res:
            showinfo('测试连接成功！', '测试连接成功！')
        else:
            showerror('测试连接失败！', '测试连接失败！')
    
    # 窗口关闭
    def close(self):
        # yes = askokcancel('是否退出？', '是否退出？')
        # if yes:
        client = FtpClient()
        if not hasattr(self, 'user'):
            self.user = 'admin'
        client.run(LOGOUT + ' %s' % self.user)
        self.master.destroy()

    # 关于
    def about(self):
        showinfo('关于', '第三组作品')

if __name__ == '__main__':
    root = Tk()
    # root.geometry('300x400')
    m = MenuBar(root)
    m.show()
    root.mainloop()