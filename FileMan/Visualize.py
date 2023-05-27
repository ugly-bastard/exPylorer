import mimetypes
import os
import curses
from curses.textpad import Textbox
from itertools import islice

editor = "code"

class Visualize:
    def __init__(self, fullScr, h, w) -> None:
        self.fullScr = fullScr
        self.lpad = curses.newpad(100, 100)
        self.mpad = curses.newpad(100, 100)
        self.rpad = curses.newpad(100, 100)
        self.cmdMode = curses.newwin(1, w-2, h-1,1)
        self.cmdWin = curses.newwin(1, w-2, h-1,2)
        self.cmdBox = Textbox(self.cmdWin)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def checkType(self, file) -> str:
        mime = mimetypes.guess_type(file)[0]
        if os.path.isdir(file):
            return "dir"
        if mime is not None:
            mime = mime.split('/')[0]
            if mime in ['audio', 'video', 'image']:
                return "media"
            elif mime in ['application']:
                return "app"
            elif mime in ['text']:
                return "text"
        return "none"

    def left(self, h,w) -> None:
        self.lpad.clear()
        menu = os.listdir("..")
        for i,text in enumerate(menu):
            self.lpad.addstr(i,1,text,curses.color_pair(1))
        self.lpad.refresh(0,0,2,2,h-2,int(25/100*w) -2)

    def mid(self, sel) -> None:
        self.mpad.clear()
        h,w = self.fullScr.getmaxyx()
        self.left(h-1,w)

        menu = os.listdir(os.getcwd())
        for i,text in enumerate(menu):
            if sel == i:
                self.mpad.addstr(i,1, text, curses.color_pair(1) | curses.A_REVERSE)
            else:
                self.mpad.addstr(i,1, text, curses.color_pair(1))
        self.mpad.refresh(0,0,2,int(25/100*w) +1,h-3,int(50/100*w) -1)

        if len(menu)>0: 
            try:
                self.right(menu[sel], h-1,w)
            except:
                self.right(menu[sel-1], h-1,w)

    def right(self, sel, h,w) -> None:
        self.rpad.clear()
        ftype = self.checkType(sel)
        if ftype == 'dir':
            try:
                menu = os.listdir(sel)
                for i,text in enumerate(menu):
                    self.rpad.addstr(i,1,text,curses.color_pair(1))
            except PermissionError:
                self.rpad.addstr(0,1,"No Permission to read directory, access denied.", curses.color_pair(1))
        else:
            if ftype == 'app':
                self.rpad.addstr("Application program", curses.color_pair(1))
            elif ftype in ['none', 'text']:
                try:
                    with open(sel) as file:
                        self.rpad.addstr(''.join(list(islice(file, h-3))), curses.color_pair(1))
                except:
                    self.rpad.addstr("Can't determine program type", curses.color_pair(1))
        self.rpad.refresh(0,0,2,int(50/100*w) +1,h-2,w-3)
