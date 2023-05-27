import mimetypes
import os
import curses
from curses.textpad import rectangle
from FileMan.Visualize import Visualize
from FileMan.Manipulate import Manipulate

editor = "code"

def manipulation(stdscr, fm, mn, menu, row):
    fm.cmdWin.clear()
    fm.cmdWin.addstr(":")
    fm.cmdBox.edit()
    text = fm.cmdBox.gather().strip()
    if text == ":dd":
        fm.cmdWin.clear()
        fm.cmdWin.addstr(f"Are you sure you want to delete {menu[row]}? y/N")
        fm.cmdWin.refresh()
        fm.cmdWin.clear()
        key = stdscr.getch()
        if key in [ord("y"), ord("Y")]:
            mn.delete(menu[row])
        fm.cmdWin.addstr(f"{menu[row]} deleted successfully!")
    elif text == ":cc":
        mn.copy(menu[row])
        fm.cmdWin.clear()
        fm.cmdWin.addstr(f"Copied {menu[row]}")
    elif text == ":xx":
        mn.cut(menu[row])
        fm.cmdWin.clear()
        fm.cmdWin.addstr(f"Cut {menu[row]}")
    elif text == ":pp":
        ret = mn.paste(os.getcwd())
        fm.cmdWin.clear()
        if ret:
            fm.cmdWin.addstr(f"Pasted {mn.copied}")
        else:
            fm.cmdWin.addstr("Nothing to paste!")
    elif text == ":touch":
        fm.cmdWin.addstr(" ")
        fm.cmdBox.edit()
        fname = fm.cmdBox.gather().strip().split(' ')[1]
        ret = mn.touch(os.getcwd()+"\\"+fname)
        fm.cmdWin.clear()
        if ret == True:
            fm.cmdWin.addstr(f"Created file {fname}")
        else:
            fm.cmdWin.addstr(ret)
    elif text == ":mkdir":
        fm.cmdWin.addstr(" ")
        fm.cmdBox.edit()
        fname = fm.cmdBox.gather().strip().split(' ')[1]
        ret = mn.mkdir(os.getcwd()+"\\"+fname)
        fm.cmdWin.clear()
        if ret == True:
            fm.cmdWin.addstr(f"Created directory {fname}")
        else:
            fm.cmdWin.addstr(ret)

    fm.cmdWin.refresh()

def main(stdscr):
    h,w = stdscr.getmaxyx()
    fm = Visualize(stdscr, h, w)
    mn = Manipulate(stdscr)
    rectangle(stdscr,1,1,h-2,int(25/100*w))
    rectangle(stdscr,1,int(25/100*w),h-2,int(50/100*w))
    rectangle(stdscr,1,int(50/100*w),h-2,w-2)

    title = curses.newwin(1,w,0,0)

    #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.use_default_colors()
    curses.curs_set(0)
    row = 0
    stdscr.refresh()
    fm.mid(row)
    while True:
        menu = os.listdir()
        title.clear()
        title.addstr(0,0,os.getcwd())
        title.refresh()
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_UP and row > 0:
            row-=1
        elif key == curses.KEY_DOWN and row < len(menu)-1:
            row+=1
        elif key == curses.KEY_LEFT:
            os.chdir("..")
            menu = os.listdir()
            row=0
        elif (key == curses.KEY_ENTER or key == curses.KEY_RIGHT) and len(menu) > 0:
            fileType = fm.checkType(menu[row])
            if fileType == "dir":
                os.chdir(menu[row])
                menu = os.listdir()
                row=0
            elif fileType == "media":
                os.system(menu[row])
            else:
                if editor == "nvim":
                    curses.endwin()
                os.system(f"{editor} {menu[row]}")
        elif (key == ord(":")):
            manipulation(stdscr, fm, mn, menu, row)
        fm.mid(row)

if __name__ == "__main__":
    mimetypes.init()
    curses.wrapper(main)
