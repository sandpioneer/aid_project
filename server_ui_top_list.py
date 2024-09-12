from tkinter import *
from tkinter.messagebox import askokcancel, showinfo, showerror
from tkinter.filedialog import askopenfilename, askdirectory
import os
from settings import *


class FileListBox:
    def __init__(self, master):
        self.master = master
        self.labelframe = LabelFrame(master, text='文件列表', padx=5, pady=5)
        self.listbox = Listbox(self.labelframe)
        self.btn_fresh_file = Button(self.labelframe, text = '刷新', command=self.display_file_list)
        self.btn_del = Button(self.labelframe, text='删除', command=self.del_file)
        self.btn_add = Button(self.labelframe, text='添加新文件', command=self.add_file)
        self.btn_open = Button(self.labelframe, text='打开文件夹', command=self.open_dir)

    # 显示在界面上
    def show(self):
        self.listbox.config({
            'bg':'lightblue',
            'height': 12,
            'width': 100
        })
        self.listbox.pack()
        self.btn_fresh_file.pack(side=LEFT, padx=5, pady=6)
        self.btn_del.pack(side=LEFT, padx=5)
        self.btn_add.pack(side=LEFT, padx=5)
        self.btn_open.pack(side=LEFT, padx=5)
        self.labelframe.pack(expand=YES, padx=10, pady=10)
    
    # 隐藏
    def hide(self):
        self.listbox.pack_forget()
    
    # 彻底销毁
    def discard(self):
        self.listbox.destroy()
    
    # 删除文件
    def del_file(self):
        selected = self.listbox.curselection()
        if len(selected) < 1:
            showerror('没有选择任何文件！', '没有选择任何文件！')
            return
        filename = self.listbox.get(selected[0])
        res = askokcancel('确定删除？', '删除后不可恢复！\n[%s]' % filename)
        if res:
            try:
                os.remove(PUBLIC_DIR + filename)
                showinfo('删除成功', '文件[%s]已删除！' % filename)
                # 刷新列表
                self.display_file_list()
            except Exception as e:
                showerror('删除失败！', e)
        
    # 获取文件列表，并显示在界面中
    def display_file_list(self):
        listdir = os.listdir(PUBLIC_DIR)
        # 清空原有内容
        self.listbox.delete(0, END)
        # 添加新内容
        for item in listdir:
            self.listbox.insert(END, item)
    
    # 添加新文件
    def add_file(self):
        filename = askopenfilename()
        try:
            fr = open(filename, 'rb')
            fw = open(PUBLIC_DIR + filename.split('/')[-1], 'wb')
            fw.write(fr.read())
        except Exception as e:
            showerror('添加新文件失败！', '添加新文件失败！' + e)
            return
        # 重新显示文件列表
        self.display_file_list()
        showinfo('添加成功！', '添加成功！\n%s' % filename)
    
    # 打开文件
    def open_dir(self):
        try:
            target = 'explorer /e,%s' % PUBLIC_DIR[:len(PUBLIC_DIR)-1]
            os.system(target)
        except Exception as e:
            showerror('该方式只适合在Windows下！', '该方式只适合在Windows下！\n' + e)

if __name__ == '__main__':
    root = Tk()
    f = FileListBox(root)
    f.show()
    f.display_file_list()
    root.mainloop()
