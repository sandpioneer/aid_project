from tkinter import *
from dbhelper import *


class UsrListBox:
    def __init__(self, master):
        self.master = master
        self.onrefresh = False
        self.labelframe = LabelFrame(master, text='在线用户列表', padx=5, pady=5)
        self.listbox = Listbox(self.labelframe)
        self.btnfresh = Button(self.labelframe, text='定时刷新:OFF', command=self.interval_refresh)
    
    def show(self):
        self.listbox.config({
            'bg': 'lightblue',
            'width': 100,
            'height': 12
        })
        self.listbox.pack(expand=YES)
        self.btnfresh.pack(padx=5, pady=5, side=LEFT)
        self.labelframe.pack(expand=YES, padx=10, pady=10)
    
    # 定时刷新开关
    def interval_refresh(self):
        self.onrefresh = not self.onrefresh
        if self.onrefresh:
            self.btnfresh.config({
                'text': '定时刷新:ON'
            })
        else:
            self.btnfresh.config({
                'text': '定时刷新:OFF'
            })
        self.display_online_usr()

    # 刷新函数
    def display_online_usr(self):
        if not self.onrefresh:
            return
        self.master.after(1500, self.display_online_usr)
        # 清空原有内容
        self.listbox.delete(0, END)
        # 添加新内容
        db = AIDHelper()
        listusr = db.usr_online_list()
        for elem in listusr:
            self.listbox.insert(END, '{:<10}{:<15}{}'.format(elem[1], elem[2], elem[3]))

if __name__ == '__main__':
    root = Tk()
    f = UsrListBox(root)
    f.show()
    f.display_online_usr()
    root.mainloop()