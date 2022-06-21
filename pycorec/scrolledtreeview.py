# scrolledtreeview.py
# https://cercopes-z.com/Python/stdlib-tkinter-widget-treeview-py.html#ex-scrollbar
from tkinter import Frame, Pack, Grid, Place
from tkinter.ttk import Treeview, Scrollbar
from tkinter.constants import HORIZONTAL, NSEW


class ScrolledTreeview(Treeview):
    def __init__(self, master=None, **kw):
        name = kw.get("name")
        if name == None:
            name = ""
        self.frame = Frame(master, name=name)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.vbar = Scrollbar(self.frame)
        self.vbar.grid(row=0, column=1, sticky="NWS")
        self.hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.hbar.grid(row=1, column=0, sticky="SWE")

        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        Treeview.__init__(self, self.frame, **kw)
        self.grid(row=0, column=0, sticky=NSEW)
        self.vbar['command'] = self.yview
        self.hbar['command'] = self.xview

        text_meths = vars(Treeview).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def forget_hbar(self):
        self.hbar.grid_forget()

    def forget_vbar(self):
        self.vbar.grid_forget()

    def __str__(self):
        return str(self.frame)
