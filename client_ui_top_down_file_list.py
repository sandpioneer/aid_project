from tkinter import *
from tkinter.messagebox import askokcancel, showinfo,showerror
from tkinter.filedialog import askopenfilename
import os
from settings import *
from client import *


class DownFileListBox:
    def __init__(self, master):
        self.master = master
        self.labelframe = LabelFrame(master, text='已下载文件列表', padx=5, pady=5)
        self.listbox = Listbox(self.labelframe)
        self.btn_fresh_file = Button(self.labelframe, text = '刷新', command=self.display_file_list)
        self.btn_del_file = Button(self.labelframe, text = '删除', command=self.del_file)
        self.btn_upload_file = Button(self.labelframe, text = '上传', command=self.upload_file)

    # 显示在界面上
    def show(self):
        self.listbox.config({
            'bg':'lightblue',
            'height': 12,
            'width': 100
        })
        self.listbox.pack()
        self.btn_fresh_file.pack(side=LEFT, padx=10, pady=5)
        self.btn_del_file.pack(side=LEFT, padx=10, pady=5)
        self.btn_upload_file.pack(side=LEFT, padx=10, pady=5)
        self.labelframe.pack(expand=YES, padx=10, pady=10)
    
    # 隐藏
    def hide(self):
        self.listbox.pack_forget()
    
    # 彻底销毁
    def discard(self):
        self.listbox.destroy()
    
    # 上传文件
    def upload_file(self):
        res = askopenfilename()
        if not res:
            print('no select')
        else:
            c = FtpClient()
            if c.run(UPLOAD + " '%s'" % res):
                showinfo('上传成功！', '上传成功！')
            else:
                showerror('上传失败！', '上传失败！')

    # 删除文件
    def del_file(self):
        selected = self.listbox.curselection()
        if len(selected) == 0:
            showerror('未选择任何文件！', '未选择任何文件！')
            return
        filename = DOWNLOAD + self.listbox.get(selected[0])
        if not askokcancel('确定删除？', '删除不可恢复！\n %s' % filename):
            return
        try:
            os.remove(filename)
            showinfo('删除成功！', '删除成功！')
            self.display_file_list()
        except Exception as e:
            showerror('删除失败！', '删除失败！\n %s' % str(e))
    
    # 获取已下载文件列表，并显示在界面中
    def display_file_list(self):
        self.listbox.delete(0, END)
        dirs = os.listdir(DOWNLOAD)
        for item in dirs:
            self.listbox.insert(END, item)

if __name__ == '__main__':
    root = Tk()
    # root.geometry('300x300')
    f = DownFileListBox(root)
    f.show()
    f.display_file_list()
    root.mainloop()
