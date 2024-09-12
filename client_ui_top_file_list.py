from tkinter import *
from tkinter.messagebox import askokcancel, showinfo,showerror
import os
from settings import *
from client import *


class FileListBox:
    def __init__(self, master, update_target=None):
        self.client = FtpClient()
        self.update_target = update_target
        self.master = master
        self.labelframe = LabelFrame(master, text='文件列表', padx=5, pady=5)
        self.listbox = Listbox(self.labelframe)
        self.btn_fresh_file = Button(self.labelframe, text = '刷新', command=self.display_file_list)
        self.btn_down_file = Button(self.labelframe, text='下载', command=self.down_file)

    # 显示在界面上
    def show(self):
        self.listbox.config({
            'bg':'lightblue',
            'height': 12,
            'width': 100
        })
        self.listbox.pack()
        self.btn_fresh_file.pack(side=LEFT, padx=10)
        self.btn_down_file.pack(side=LEFT, padx=5, pady=5)
        self.labelframe.pack(expand=YES, padx=10, pady=10)
    
    # 隐藏
    def hide(self):
        self.listbox.pack_forget()
    
    # 彻底销毁
    def discard(self):
        self.listbox.destroy()
    
    # 下载文件
    def down_file(self):
        selected = self.listbox.curselection()
        if len(selected) < 1:
            showerror('没有选择任何文件！', '没有选择任何文件！')
            return
        filename = self.listbox.get(selected[0])
        res = askokcancel('确定下载？', '将下载以下内容\n%s' % filename)
        if not res:
            return
        try:
            if self.client.run(self.organize_cmd(DOWN, filename)):
                showinfo('下载成功', '文件 [%s] 下载完成！' % filename)
                self.update_down_file_list()
            else:
                showerror('服务器拒绝下载！', '下载失败！')
            
        except Exception as e:
            showerror('下载失败！', e)
        
    # 获取文件列表，并显示在界面中
    def display_file_list(self):
        # 获取当前选中项
        selected = self.listbox.curselection()
        if len(selected) == 0:
            dirlist = self.client.run(self.organize_cmd(LIST))
        else:
            filename = self.listbox.get(selected[0])
            dirlist = self.client.run(self.organize_cmd(LIST, filename))
        # 未获取到任何内容
        if type(dirlist) is bool:
            showerror('连接服务器失败！', '连接服务器失败！')
            return
        # 清空原有内容
        self.listbox.delete(0, END)
        # 添加新内容
        for item in dirlist:
            self.listbox.insert(END, item)
    
    # 显示已下载文件
    def update_down_file_list(self):
        if not self.update_target:
            return
        self.update_target.display_file_list()

    # 组织命令格式
    def organize_cmd(self, cmd, *args):
        command = cmd
        for item in args:
            command += "'%s'" % item
        return command

if __name__ == '__main__':
    root = Tk()
    # root.geometry('300x300')
    f = FileListBox(root)
    f.show()
    f.display_file_list()
    root.mainloop()
