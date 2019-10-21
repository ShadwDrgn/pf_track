import os
import requests
import json
import tkinter
from tkinter import Tk

class UI():
    def __init__(self):
        self.monsters = load_data('monster_analysis.json')
        self.root = Tk()
        self.root.title('Initiative')
        self.frame_main = tkinter.Frame(self.root,width=800)
        self.frame_main.pack(padx=6,pady=6, fill='both')
        self.frame_type = tkinter.Frame(self.frame_main)
        self.frame_type.grid(row=0,column=0,sticky='n')
        self.mon_type = tkinter.StringVar()
        TYPES = {'Type':'type','CR': 'cr', 'SubType':'subtypes'}
        self.mon_type.set('subtypes')
        for i,k in enumerate(TYPES):
            r = tkinter.Radiobutton(self.frame_type,text=k,variable=self.mon_type,value=TYPES[k]).grid(row=0,column=i, sticky='wn')
            print(f'Col: {i}, Text: {TYPES[k]}')
        self.list_type = tkinter.Listbox(self.frame_main,height=20,exportselection=False)
        self.list_type.grid(row=1,column=0,sticky='wns')
        self.stype = tkinter.StringVar()
        self.entry_search = tkinter.Entry(self.frame_main,textvariable=self.stype).grid(column=0,row=2,sticky='nw')
        self.stype.trace('w',self.populate_type)
        self.populate_type()
        self.list_monsters = tkinter.Listbox(self.frame_main,exportselection=False)
        self.list_monsters.grid(column=1,row=1,sticky='wns')
        self.list_type.bind('<<ListboxSelect>>',self.on_monster)


    def on_monster(self,evt):
        sel = evt.widget.curselection()
        if not sel:
            return
        i = int(sel[0])
        tval = evt.widget.get(i)
        self.populate_monsters(tval)


    def populate_monsters(self,tval):
        mon_type = self.mon_type.get()
        if mon_type == 'subtypes':
            mons = [mon['name'] for mon in self.monsters if mon_type in mon and mon[mon_type] is not None and any(tval in s for s in mon[mon_type])]
        self.list_monsters.delete(0,'end')
        for mon in mons:
            self.list_monsters.insert('end',mon)

    def populate_type(self,*args):
        stype =self.stype.get()
        mon_type = self.mon_type.get()
        if mon_type == 'subtypes':
            types = [mon[mon_type] for mon in self.monsters if mon_type in mon and mon[mon_type] is not None and any(stype in s for s in mon[mon_type])]
            nt = set()
            for l in types:
                for st in l:
                    if stype in st:
                        nt.add(st)
            types = nt
        else:
            types = set([mon[mon_type] for mon in self.monsters if mon_type in mon and mon[mon_type] is not None and stype in mon[mon_type]])
        self.list_type.delete(0,'end')
        for mtype in types:
            if mtype is not None:
                self.list_type.insert('end', mtype)



def load_data(file):
    if not os.path.exists(file):
        with open(file,'w') as f:
            data = requests.get('https://rpgbot.net/pathfinder/js/monster_analysis.json').json()
            f.write(json.dumps(data))
    else:
        with open(file,'r', encoding='utf8') as f:
            data=json.loads(f.read())
    return data


def main():

    ui = UI()
    ui.root.mainloop()


if __name__ == '__main__':
    main()