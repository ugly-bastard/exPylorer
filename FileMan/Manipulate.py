import os
import curses
import shutil

class Manipulate:
    def __init__(self, fullScr) -> None:
        self.fullScr = fullScr
        self.toCopy = None
        self.copied = None
        self.pasted = None

    def touch(self, path):
        try:
            with open(path, 'a'):
                os.utime(path, None)
            return True
        except Exception as e:
            return e

    def mkdir(self, path):
        try:
            os.mkdir(path)
            return True
        except Exception as e:
            return e

    def delete(self, path) -> None:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            if not os.listdir():
                os.rmdir(path)
            else:
                shutil.rmtree(path)

    def copy(self, path) -> None:
        self.copied = os.path.abspath(path)
        self.toCopy = True
        self.pasted = False

    def cut(self, path) -> None:
        self.copied = os.path.abspath(path)
        self.toCopy = False
        self.pasted = False

    def paste(self, path):
        if not self.pasted:
            path = path + "\\" + self.copied.split("\\")[-1:][0]
            if self.toCopy:
                shutil.copy(self.copied, path)
            elif not self.toCopy:
                shutil.move(self.copied, path)
            self.pasted = True
            return True
        else:
            return False
