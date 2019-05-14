from tkinter import *


class RegModule:
    def __init__(self, master):
        self.frame = LabelFrame(master, text='用户注册', padx=60, pady=30)
        self.master = master
    
    # 创建组件，并且布局完毕
    def create_component(self):
        self.labeluname = Label(self.frame, text='用户名', anchor='nw')
        self.labelupwd = Label(self.frame, text='密码', anchor='nw')
        self.labelconfirm = Label(self.frame, text='重复一次', anchor='nw')
        self.entryuname = Entry(self.frame)
        self.entryunpwd = Entry(self.frame, show='*')
        self.entryconfirm = Entry(self.frame, show='*')
        
        self.labeluname.pack(fill=X)
        self.entryuname.pack()
        self.labelupwd.pack(fill=X)
        self.entryunpwd.pack()
        self.labelconfirm.pack(fill=X)
        self.entryconfirm.pack()

        # 确定按钮
        self.btnok = Button(self.frame, text='确定')
        self.btnok.pack(side=LEFT, pady=10, padx=10)
        # 取消
        self.btncancel = Button(self.frame, text='取消', command=self.master.quit)
        self.btncancel.pack(side=RIGHT)

    # 显示frame
    def show(self):
        self.frame.pack(expand=YES, padx=100, pady=50)
    
    # 隐藏frame
    def hide(self):
        self.frame.pack_forget()
    
    # 销毁
    def discard(self, *args):
        self.frame.destroy()

if __name__ == '__main__':
    root = Tk()
    l = RegModule(root)
    l.create_component()
    l.show()
    mainloop()