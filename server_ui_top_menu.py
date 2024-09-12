from tkinter import *
from tkinter.messagebox import showinfo, showerror
from server import *
from multiprocessing import Process

class MenuBar:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.menubar = Menu(master)
        self.run_server = None

    # 将菜单显示出来
    def show(self):
        # 文件菜单
        self.filemenu = Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label='启动服务器', command=self.start_server)
        self.filemenu.add_command(label='关闭服务器', command=self.stop_server)
        # filemenu.add_command(label='保存')
        self.filemenu.add_command(label='退出', command=self.master.quit)
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

    # 启动服务选项
    def start_server(self):
        if self.run_server:
            showerror('警告！', '服务器已启动！')
            return
        p = Process(target=FtpServer().run_forever)
        p.daemon = True
        p.start()
        self.run_server = True
        print('FTP服务器%s已启动...' % str(SERVER_ADDR))
        showinfo('FTP服务器已启动','FTP服务器已启动')
        return True

    # 停止服务
    def stop_server(self):
        showerror('停止服务', '该功能正在开发！')
    
    # 关于
    def about(self):
        showinfo('关于', '第三组作品')

if __name__ == '__main__':
    root = Tk()
    # root.geometry('300x400')
    m = MenuBar(root)
    m.show()
    root.mainloop()