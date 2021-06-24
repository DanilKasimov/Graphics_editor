from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from math import *
import random as rand
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import easygui

Triangles = []
lines = []
lines3D = []
Figures3D = []
Figures = []
window = Tk()
index = [0, 0]
width = window.winfo_screenwidth() - 10
height = window.winfo_screenheight() - 70
window.geometry('{}x{}+0+0'.format(width, height))
window.title("Графический редактор")
can = Canvas(window, width=width, height=height, bg='white')
Formul = Entry(width=80, bd=2)
DeleteBtn = Button(width=20, text='Удалить')
UnionBtn = Button(width=20, text='Объединить')
SplineBtn = Button(width=20, text='В3 Сплайн')
SplineBtn.place(x=900, y=0)
AddBtn = Button(width=20, text='Создать объект')
DownLoadBtn = Button(width=20, text='Загрузить из файла')
DownLoadBtn.place(x=600, y=0)
SaveBtn = Button(width=20, text='Сохранить в файл')
SaveBtn.place(x=750, y=0)
DisUnionBtn = Button(width=20, text='Разъединить')
DisUnionBtn.place(x=450, y=0)
UnionBtn.place(x=0, y=0)
DeleteBtn.place(x=150, y=0)
AddBtn.place(x=300, y=0)
Formul.place(y=height - 20, x=width - width / 4 + 2)
Labx1 = Label(text="x1=", font=("Comic Sans MS", 12), bg="white")
Labx1.place(y=20, x=width - width / 4 + 2)
Laby1 = Label(text="y1=", font=("Comic Sans MS", 12), bg="white")
Laby1.place(y=70, x=width - width / 4 + 2)
Labz1 = Label(text="z1=", font=("Comic Sans MS", 12), bg="white")
Labz1.place(y=120, x=width - width / 4 + 2)
Labx2 = Label(text="x2=", font=("Comic Sans MS", 12), bg="white")
Labx2.place(y=20, x=width - width / 8 - 20)
Laby2 = Label(text="y2=", font=("Comic Sans MS", 12), bg="white")
Laby2.place(y=70, x=width - width / 8 - 20)
Labz2 = Label(text="z2=", font=("Comic Sans MS", 12), bg="white")
Labz2.place(y=120, x=width - width / 8 - 20)
Entx1 = Entry(width=25, bd=2)
Entx1.place(y=25, x=width - width / 4 + 35)
Enty1 = Entry(width=25, bd=2)
Enty1.place(y=75, x=width - width / 4 + 35)
Entz1 = Entry(width=25, bd=2)
Entz1.place(y=125, x=width - width / 4 + 35)
Entx2 = Entry(width=25, bd=2)
Entx2.place(y=25, x=width - width / 8 + 25)
Enty2 = Entry(width=25, bd=2)
Enty2.place(y=75, x=width - width / 8 + 25)
Entz2 = Entry(width=25, bd=2)
Entz2.place(y=125, x=width - width / 8 + 25)
ReBuild = Button(width=20, text='Перестроить линию')
ReBuild.place(x=width - ((width / 8 + 25) + (width / 4 + 35)) / 2 + 50, y=150)
text1 = Label(text="Морфинг", font=("Comic Sans MS", 15), bg="white")
text1.place(x=width - ((width / 8 + 25) + (width / 4 + 35)) / 2 + 80, y=200)
Morph = Scale(window, from_=1, to=10, orient=HORIZONTAL, length=200)
Morph.place(x=width - ((width / 8 + 25) + (width / 4 + 35)) / 2 + 30, y=250)
Lr = Label(text="R", font=("Comic Sans MS", 16), bg="white")
Lg = Label(text="G", font=("Comic Sans MS", 16), bg="white")
Lb = Label(text="B", font=("Comic Sans MS", 16), bg="white")
Lr.place(x=width - width / 4 + 50, y=320)
Lg.place(x=width - width / 4 + 100, y=320)
Lb.place(x=width - width / 4 + 150, y=320)
R = Scale(window, from_=0, to=255, orient=VERTICAL, length=200)
R.place(x=width - width / 4 + 40, y=360)
G = Scale(window, from_=0, to=255, orient=VERTICAL, length=200)
G.place(x=width - width / 4 + 90, y=360)
B = Scale(window, from_=0, to=255, orient=VERTICAL, length=200)
B.place(x=width - width / 4 + 140, y=360)
Look = Scale(window, from_=0, to=100, orient=HORIZONTAL, length=200)
Look.place(x=width - width / 4 + 10, y=600)
can.pack()
can.create_line(width - width / 4, 0, width - width / 4, height, fill='black', width='3')
can.create_line(width - width / 4, height - height / 3, width, height - height / 3, fill='black', width='3')
zc = 0.001


class Point3D:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, a, b, c):
        self.x = a
        self.y = b
        self.z = c

    def Copy(self):
        return Point3D(self.x, self.y, self.z)


def higlighter(line):
    Entx1.delete(0, 'end')
    Entx1.insert(0, str(line.Point1.x))
    Entx2.delete(0, 'end')
    Entx2.insert(0, str(line.Point2.x))
    Enty1.delete(0, 'end')
    Enty1.insert(0, str(line.Point1.y))
    Enty2.delete(0, 'end')
    Enty2.insert(0, str(line.Point2.y))
    Entz1.delete(0, 'end')
    Entz1.insert(0, str(line.Point1.z))
    Entz2.delete(0, 'end')
    Entz2.insert(0, str(line.Point2.z))


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


class Figure:
    High = False

    def __init__(self, a):
        self.Lines = []
        for i in range(len(a)):
            self.Lines.append(a[i])
            self.DrawFig()

    def DrawFig(self):
        for i in range(len(self.Lines)):
            self.Lines[i].DrawLine()

    def FitFig(self, event):
        for i in range(len(self.Lines)):
            if self.Lines[i].Fit(event):
                return True
        return False

    def RedLy(self):
        for i in range(len(self.Lines)):
            can.itemconfig(self.Lines[i].idLine, fill=_from_rgb((255, 0, 0)))
            can.itemconfig(self.Lines[i].idLeft, fill=_from_rgb((255, 0, 0)))
            can.itemconfig(self.Lines[i].idRight, fill=_from_rgb((255, 0, 0)))

    def Blackly(self):
        for i in range(len(self.Lines)):
            can.itemconfig(self.Lines[i].idLine, fill=_from_rgb((self.Lines[i].r, self.Lines[i].g, self.Lines[i].b)))
            can.itemconfig(self.Lines[i].idLeft, fill=_from_rgb((self.Lines[i].r, self.Lines[i].g, self.Lines[i].b)))
            can.itemconfig(self.Lines[i].idRight, fill=_from_rgb((self.Lines[i].r, self.Lines[i].g, self.Lines[i].b)))

    def X0(self):
        x0 = 0
        for i in range(len(self.Lines)):
            x0 += self.Lines[i].Point1.x + self.Lines[i].Point2.x
        return x0 / (len(self.Lines) * 2)

    def Y0(self):
        y0 = 0
        for i in range(len(self.Lines)):
            y0 += self.Lines[i].Point1.y + self.Lines[i].Point2.y
        return y0 / (len(self.Lines) * 2)

    def Z0(self):
        z0 = 0
        for i in range(len(self.Lines)):
            z0 += self.Lines[i].Point1.z + self.Lines[i].Point2.z
        return z0 / (len(self.Lines) * 2)

    def MoveFig(self, event):
        m = self.X0()
        n = self.Y0()
        ok = False
        for i in range(len(self.Lines)):
            if self.Lines[i].FitRes(event):
                self.Lines[i].Resize(event)
                ok = True
        if ok:
            return
        for i in range(len(self.Lines)):
            x = self.Lines[i].Point1.x
            y = self.Lines[i].Point1.y
            self.Lines[i].Point1.x = x + event.x - m
            self.Lines[i].Point1.y = y + event.y - n
            x = self.Lines[i].Point2.x
            y = self.Lines[i].Point2.y
            self.Lines[i].Point2.x = x + event.x - m
            self.Lines[i].Point2.y = y + event.y - n
        self.DrawFig()

    def RotateFig(self, event):
        m = self.X0()
        n = self.Y0()
        for i in range(len(self.Lines)):
            if event.delta > 0:
                s = sin(pi / 12)
                c = cos(pi / 12)
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point1.y = c * (y - n) + s * (x - m) + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point2.y = c * (y - n) + s * (x - m) + n
            else:
                s = sin(-pi / 12)
                c = cos(-pi / 12)
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point1.y = c * (y - n) + s * (x - m) + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point2.y = c * (y - n) + s * (x - m) + n
        self.DrawFig()

    def RotateXUp(self):
        for i in self.Lines:
            i.Point1.x = i.Point1.x * (zc * i.Point1.z + 1)
            i.Point1.y = i.Point1.y * (zc * i.Point1.z + 1)
            i.Point2.x = i.Point2.x * (zc * i.Point2.z + 1)
            i.Point2.y = i.Point2.y * (zc * i.Point2.z + 1)
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        c = cos(pi / 12)
        s = sin(pi / 12)
        for i in self.Lines:
            x = i.Point1.x
            y = i.Point1.y
            z = i.Point1.z
            i.Point1.x = x
            i.Point1.y = c * (y - n) + s * (z - k) + n
            i.Point1.z = s * (n - y) + c * (z - k) + k
            x = i.Point2.x
            y = i.Point2.y
            z = i.Point2.z
            i.Point2.x = x
            i.Point2.y = c * (y - n) + s * (z - k) + n
            i.Point2.z = s * (n - y) + c * (z - k) + k
            i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
            i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
            i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
            i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
        self.DrawFig()

    def RotateXdwn(self):
        for i in self.Lines:
            i.Point1.x = i.Point1.x * (zc * i.Point1.z + 1)
            i.Point1.y = i.Point1.y * (zc * i.Point1.z + 1)
            i.Point2.x = i.Point2.x * (zc * i.Point2.z + 1)
            i.Point2.y = i.Point2.y * (zc * i.Point2.z + 1)
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        c = cos(-pi / 12)
        s = sin(-pi / 12)
        for i in self.Lines:
            x = i.Point1.x
            y = i.Point1.y
            z = i.Point1.z
            i.Point1.x = x
            i.Point1.y = c * (y - n) + s * (z - k) + n
            i.Point1.z = s * (n - y) + c * (z - k) + k
            x = i.Point2.x
            y = i.Point2.y
            z = i.Point2.z
            i.Point2.x = x
            i.Point2.y = c * (y - n) + s * (z - k) + n
            i.Point2.z = s * (n - y) + c * (z - k) + k
            i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
            i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
            i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
            i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
        self.DrawFig()

    def RotateYL(self):
        for i in self.Lines:
            i.Point1.x = i.Point1.x * (zc * i.Point1.z + 1)
            i.Point1.y = i.Point1.y * (zc * i.Point1.z + 1)
            i.Point2.x = i.Point2.x * (zc * i.Point2.z + 1)
            i.Point2.y = i.Point2.y * (zc * i.Point2.z + 1)
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        c = cos(-pi / 12)
        s = sin(-pi / 12)
        for i in self.Lines:
            x = i.Point1.x
            y = i.Point1.y
            z = i.Point1.z
            i.Point1.x = c * (x - m) + s * (z - k) + m
            i.Point1.y = y
            i.Point1.z = s * (m - x) + c * (z - k) + k
            x = i.Point2.x
            y = i.Point2.y
            z = i.Point2.z
            i.Point2.x = c * (x - m) + s * (z - k) + m
            i.Point2.y = y
            i.Point2.z = s * (m - x) + c * (z - k) + k
            i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
            i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
            i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
            i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
        self.DrawFig()

    def RotateYR(self):
        for i in self.Lines:
            i.Point1.x = i.Point1.x * (zc * i.Point1.z + 1)
            i.Point1.y = i.Point1.y * (zc * i.Point1.z + 1)
            i.Point2.x = i.Point2.x * (zc * i.Point2.z + 1)
            i.Point2.y = i.Point2.y * (zc * i.Point2.z + 1)
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        c = cos(pi / 12)
        s = sin(pi / 12)
        for i in self.Lines:
            x = i.Point1.x
            y = i.Point1.y
            z = i.Point1.z
            i.Point1.x = c * (x - m) + s * (z - k) + m
            i.Point1.y = y
            i.Point1.z = s * (m - x) + c * (z - k) + k
            x = i.Point2.x
            y = i.Point2.y
            z = i.Point2.z
            i.Point2.x = c * (x - m) + s * (z - k) + m
            i.Point2.y = y
            i.Point2.z = s * (m - x) + c * (z - k) + k
            i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
            i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
            i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
            i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
        self.DrawFig()

    def RotateZR(self):
        for i in self.Lines:
            i.Point1.x = i.Point1.x * (zc * i.Point1.z + 1)
            i.Point1.y = i.Point1.y * (zc * i.Point1.z + 1)
            i.Point2.x = i.Point2.x * (zc * i.Point2.z + 1)
            i.Point2.y = i.Point2.y * (zc * i.Point2.z + 1)
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        c = cos(pi / 12)
        s = sin(pi / 12)
        for i in self.Lines:
            x = i.Point1.x
            y = i.Point1.y
            z = i.Point1.z
            i.Point1.x = c * (x - m) + s * (n - y) + m
            i.Point1.y = s * (x - m) + c * (y - n) + n
            i.Point1.z = z
            x = i.Point2.x
            y = i.Point2.y
            z = i.Point2.z
            i.Point2.x = c * (x - m) + s * (n - y) + m
            i.Point2.y = s * (x - m) + c * (y - n) + n
            i.Point2.z = z
            i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
            i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
            i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
            i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
        self.DrawFig()

    def RotateZL(self):
        for i in self.Lines:
            i.Point1.x = i.Point1.x * (zc * i.Point1.z + 1)
            i.Point1.y = i.Point1.y * (zc * i.Point1.z + 1)
            i.Point2.x = i.Point2.x * (zc * i.Point2.z + 1)
            i.Point2.y = i.Point2.y * (zc * i.Point2.z + 1)
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        c = cos(-pi / 12)
        s = sin(-pi / 12)
        for i in self.Lines:
            x = i.Point1.x
            y = i.Point1.y
            z = i.Point1.z
            i.Point1.x = c * (x - m) + s * (n - y) + m
            i.Point1.y = s * (x - m) + c * (y - n) + n
            i.Point1.z = z
            x = i.Point2.x
            y = i.Point2.y
            z = i.Point2.z
            i.Point2.x = c * (x - m) + s * (n - y) + m
            i.Point2.y = s * (x - m) + c * (y - n) + n
            i.Point2.z = z
            i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
            i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
            i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
            i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
        self.DrawFig()

    def MirrorFig(self, event):
        m = self.X0()
        n = self.Y0()
        k = self.Z0()
        if event.char == 'z':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * (-1) + 2 * m
                self.Lines[i].Point1.y = y
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * (-1) + 2 * m
                self.Lines[i].Point2.y = y
        if event.char == 'x':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x
                self.Lines[i].Point1.y = y * (-1) + 2 * n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x
                self.Lines[i].Point2.y = y * (-1) + 2 * n
        if event.char == 'c':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * (self.Lines[i].Point1.z * zc + 1)
                self.Lines[i].Point1.y = y * (self.Lines[i].Point1.z * zc + 1)
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * (self.Lines[i].Point2.z * zc + 1)
                self.Lines[i].Point2.y = y * (self.Lines[i].Point2.z * zc + 1)
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                z = self.Lines[i].Point1.z
                self.Lines[i].Point1.x = x
                self.Lines[i].Point1.y = y
                self.Lines[i].Point1.z = (-1) * z + 2 * k
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                z = self.Lines[i].Point2.z
                self.Lines[i].Point2.x = x
                self.Lines[i].Point2.y = y
                self.Lines[i].Point2.z = (-1) * z + 2 * k
                self.Lines[i].Point1.x = self.Lines[i].Point1.x / (self.Lines[i].Point1.z * zc + 1)
                self.Lines[i].Point1.y = self.Lines[i].Point1.y / (self.Lines[i].Point1.z * zc + 1)
                self.Lines[i].Point2.x = self.Lines[i].Point2.x / (self.Lines[i].Point2.z * zc + 1)
                self.Lines[i].Point2.y = self.Lines[i].Point2.y / (self.Lines[i].Point2.z * zc + 1)
        self.DrawFig()

    def ScaleFig(self, event):
        m = self.X0()
        n = self.Y0()
        if event.char == 'q':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * 1.1 - m * 1.1 + m
                self.Lines[i].Point1.y = y * 1.1 - n * 1.1 + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * 1.1 - m * 1.1 + m
                self.Lines[i].Point2.y = y * 1.1 - n * 1.1 + n
        if event.char == 'w':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * 0.9 - m * 0.9 + m
                self.Lines[i].Point1.y = y * 0.9 - n * 0.9 + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * 0.9 - m * 0.9 + m
                self.Lines[i].Point2.y = y * 0.9 - n * 0.9 + n
        self.DrawFig()


class Line:
    High = False
    idLine = ""
    Point1 = None
    Point2 = None
    idLeft = ""
    idRight = ""

    def __init__(self, P1, P2):
        self.r = 0
        self.g = 0
        self.b = 0
        self.Point1 = P1
        self.Point2 = P2
        self.idLine = can.create_line(P1.x, P1.y, P2.x, P2.y, fill=_from_rgb((self.r, self.g, self.b)))
        self.idLeft = can.create_oval(P1.x - 5, P1.y - 5, P1.x + 5, P1.y + 5, fill=_from_rgb((self.r, self.g, self.b)))
        self.idRight = can.create_oval(P2.x - 5, P2.y - 5, P2.x + 5, P2.y + 5, fill=_from_rgb((self.r, self.g, self.b)))

    def DrawLine(self):
        can.coords(self.idLine, self.Point1.x, self.Point1.y, self.Point2.x, self.Point2.y)
        can.coords(self.idLeft, self.Point1.x - 5, self.Point1.y - 5, self.Point1.x + 5, self.Point1.y + 5)
        can.coords(self.idRight, self.Point2.x - 5, self.Point2.y - 5, self.Point2.x + 5, self.Point2.y + 5)
        can.itemconfig(self.idLine, fill=_from_rgb((self.r, self.g, self.b)))
        can.itemconfig(self.idRight, fill=_from_rgb((self.r, self.g, self.b)))
        can.itemconfig(self.idLeft, fill=_from_rgb((self.r, self.g, self.b)))
        higlighter(self)
        Formul.delete(0, 'end')
        Formul.insert(0, "{}A+{}B+{}=0".format(self.Point1.y - self.Point2.y, self.Point2.x - self.Point1.x,
                                               self.Point1.x * self.Point2.y - self.Point2.x * self.Point1.y))

    def Fit(self, event):
        # (y1-y2)x+(x2-x1)y+(x1*y2-x2*y1)=0 - уравнение прямой лежащей на двух точках
        if abs((self.Point1.y - self.Point2.y) * event.x + (self.Point2.x - self.Point1.x) * event.y +
               (self.Point1.x * self.Point2.y - self.Point2.x * self.Point1.y)) / sqrt(
            (self.Point1.y - self.Point2.y + 0.1) ** 2 +
            (self.Point2.x - self.Point1.x + 0.1) ** 2) <= 3 and (
                (self.Point1.x - 7 <= event.x <= self.Point2.x + 7) or (
                self.Point2.x - 7 <= event.x <= self.Point1.x + 7)):
            return True
        else:
            return False

    def FitRes(self, event):
        if (self.Point2.x - event.x) ** 2 + (self.Point2.y - event.y) ** 2 <= 49 or (self.Point1.x - event.x) ** 2 + (
                self.Point1.y - event.y) ** 2 <= 49:
            return True
        else:
            return False

    def Resize(self, event):
        if (self.Point2.x - event.x) ** 2 + (self.Point2.y - event.y) ** 2 <= 49:
            self.Point2.x = event.x
            self.Point2.y = event.y
            self.DrawLine()
            return
        elif (self.Point1.x - event.x) ** 2 + (self.Point1.y - event.y) ** 2 <= 49:
            self.Point1.x = event.x
            self.Point1.y = event.y
            self.DrawLine()
            return

    def Move(self, event):
        if (self.Point2.x - event.x) ** 2 + (self.Point2.y - event.y) ** 2 <= 49 or (self.Point1.x - event.x) ** 2 + (
                self.Point1.y - event.y) ** 2 <= 49:
            self.Resize(event)
            return
        else:
            deltax = (self.Point1.x + self.Point2.x) / 2
            deltay = (self.Point1.y + self.Point2.y) / 2
            self.Point1.x = event.x + self.Point1.x - deltax
            self.Point1.y = event.y + self.Point1.y - deltay
            self.Point2.x = event.x + self.Point2.x - deltax
            self.Point2.y = event.y + self.Point2.y - deltay
            self.DrawLine()

    def Rotate(self, event):
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        if event.delta > 0:
            s = sin(pi / 12)
            c = cos(pi / 12)
            x = self.Point1.x
            y = self.Point1.y
            self.Point1.x = c * (x - m) + s * (n - y) + m
            self.Point1.y = c * (y - n) + s * (x - m) + n
            x = self.Point2.x
            y = self.Point2.y
            self.Point2.x = c * (x - m) + s * (n - y) + m
            self.Point2.y = c * (y - n) + s * (x - m) + n
            self.DrawLine()
        else:
            s = sin(-pi / 12)
            c = cos(-pi / 12)
            x = self.Point1.x
            y = self.Point1.y
            self.Point1.x = c * (x - m) + s * (n - y) + m
            self.Point1.y = c * (y - n) + s * (x - m) + n
            x = self.Point2.x
            y = self.Point2.y
            self.Point2.x = c * (x - m) + s * (n - y) + m
            self.Point2.y = c * (y - n) + s * (x - m) + n
            self.DrawLine()

    def RotateXup(self):
        self.Point1.x = self.Point1.x * (zc * self.Point1.z + 1)
        self.Point1.y = self.Point1.y * (zc * self.Point1.z + 1)
        self.Point2.x = self.Point2.x * (zc * self.Point2.z + 1)
        self.Point2.y = self.Point2.y * (zc * self.Point2.z + 1)
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        k = (self.Point1.z + self.Point2.z) / 2
        s = sin(pi / 12)
        c = cos(pi / 12)
        x = self.Point1.x
        y = self.Point1.y
        z = self.Point1.z
        self.Point1.x = x
        self.Point1.y = cos(pi / 12) * (y - n) + sin(pi / 12) * (z - k) + n
        self.Point1.z = sin(pi / 12) * (n - y) + cos(pi / 12) * (z - k) + k
        x = self.Point2.x
        y = self.Point2.y
        z = self.Point2.z
        self.Point2.x = x
        self.Point2.y = cos(pi / 12) * (y - n) + sin(pi / 12) * (z - k) + n
        self.Point2.z = sin(pi / 12) * (n - y) + cos(pi / 12) * (z - k) + k
        self.Point1.x = self.Point1.x / (self.Point1.z * zc + 1)
        self.Point1.y = self.Point1.y / (self.Point1.z * zc + 1)
        self.Point2.x = self.Point2.x / (self.Point2.z * zc + 1)
        self.Point2.y = self.Point2.y / (self.Point2.z * zc + 1)
        self.DrawLine()

    def RotateXdwn(self):
        self.Point1.x = self.Point1.x * (zc * self.Point1.z + 1)
        self.Point1.y = self.Point1.y * (zc * self.Point1.z + 1)
        self.Point2.x = self.Point2.x * (zc * self.Point2.z + 1)
        self.Point2.y = self.Point2.y * (zc * self.Point2.z + 1)
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        k = (self.Point1.z + self.Point2.z) / 2
        s = sin(pi / 12)
        c = cos(pi / 12)
        x = self.Point1.x
        y = self.Point1.y
        z = self.Point1.z
        self.Point1.x = x
        self.Point1.y = cos(-pi / 12) * (y - n) + sin(-pi / 12) * (z - k) + n
        self.Point1.z = sin(-pi / 12) * (n - y) + cos(-pi / 12) * (z - k) + k
        x = self.Point2.x
        y = self.Point2.y
        z = self.Point2.z
        self.Point2.x = x
        self.Point2.y = cos(-pi / 12) * (y - n) + sin(-pi / 12) * (z - k) + n
        self.Point2.z = sin(-pi / 12) * (n - y) + cos(-pi / 12) * (z - k) + k
        self.Point1.x = self.Point1.x / (self.Point1.z * zc + 1)
        self.Point1.y = self.Point1.y / (self.Point1.z * zc + 1)
        self.Point2.x = self.Point2.x / (self.Point2.z * zc + 1)
        self.Point2.y = self.Point2.y / (self.Point2.z * zc + 1)
        self.DrawLine()

    def RotateYR(self):
        self.Point1.x = self.Point1.x * (zc * self.Point1.z + 1)
        self.Point1.y = self.Point1.y * (zc * self.Point1.z + 1)
        self.Point2.x = self.Point2.x * (zc * self.Point2.z + 1)
        self.Point2.y = self.Point2.y * (zc * self.Point2.z + 1)
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        k = (self.Point1.z + self.Point2.z) / 2
        s = sin(pi / 12)
        c = cos(pi / 12)
        x = self.Point1.x
        y = self.Point1.y
        z = self.Point1.z
        self.Point1.x = c * (x - m) + s * (z - k) + m
        self.Point1.y = y
        self.Point1.z = s * (m - x) + c * (z - k) + k
        x = self.Point2.x
        y = self.Point2.y
        z = self.Point2.z
        self.Point2.x = c * (x - m) + s * (z - k) + m
        self.Point2.y = y
        self.Point2.z = s * (m - x) + c * (z - k) + k
        self.Point1.x = self.Point1.x / (self.Point1.z * zc + 1)
        self.Point1.y = self.Point1.y / (self.Point1.z * zc + 1)
        self.Point2.x = self.Point2.x / (self.Point2.z * zc + 1)
        self.Point2.y = self.Point2.y / (self.Point2.z * zc + 1)
        self.DrawLine()

    def RotateYL(self):
        self.Point1.x = self.Point1.x * (zc * self.Point1.z + 1)
        self.Point1.y = self.Point1.y * (zc * self.Point1.z + 1)
        self.Point2.x = self.Point2.x * (zc * self.Point2.z + 1)
        self.Point2.y = self.Point2.y * (zc * self.Point2.z + 1)
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        k = (self.Point1.z + self.Point2.z) / 2
        s = sin(-pi / 12)
        c = cos(-pi / 12)
        x = self.Point1.x
        y = self.Point1.y
        z = self.Point1.z
        self.Point1.x = c * (x - m) + s * (z - k) + m
        self.Point1.y = y
        self.Point1.z = s * (m - x) + c * (z - k) + k
        x = self.Point2.x
        y = self.Point2.y
        z = self.Point2.z
        self.Point2.x = c * (x - m) + s * (z - k) + m
        self.Point2.y = y
        self.Point2.z = s * (m - x) + c * (z - k) + k
        self.Point1.x = self.Point1.x / (self.Point1.z * zc + 1)
        self.Point1.y = self.Point1.y / (self.Point1.z * zc + 1)
        self.Point2.x = self.Point2.x / (self.Point2.z * zc + 1)
        self.Point2.y = self.Point2.y / (self.Point2.z * zc + 1)
        self.DrawLine()

    def RotateZR(self):
        self.Point1.x = self.Point1.x * (zc * self.Point1.z + 1)
        self.Point1.y = self.Point1.y * (zc * self.Point1.z + 1)
        self.Point2.x = self.Point2.x * (zc * self.Point2.z + 1)
        self.Point2.y = self.Point2.y * (zc * self.Point2.z + 1)
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        k = (self.Point1.z + self.Point2.z) / 2
        s = sin(pi / 12)
        c = cos(pi / 12)
        x = self.Point1.x
        y = self.Point1.y
        z = self.Point1.z
        self.Point1.x = c * (x - m) + s * (n - y) + m
        self.Point1.y = s * (x - m) + c * (y - n) + n
        self.Point1.z = z
        x = self.Point2.x
        y = self.Point2.y
        z = self.Point2.z
        self.Point2.x = c * (x - m) + s * (n - y) + m
        self.Point2.y = s * (x - m) + c * (y - n) + n
        self.Point2.z = z
        self.Point1.x = self.Point1.x / (self.Point1.z * zc + 1)
        self.Point1.y = self.Point1.y / (self.Point1.z * zc + 1)
        self.Point2.x = self.Point2.x / (self.Point2.z * zc + 1)
        self.Point2.y = self.Point2.y / (self.Point2.z * zc + 1)
        self.DrawLine()

    def RotateZL(self):
        self.Point1.x = self.Point1.x * (zc * self.Point1.z + 1)
        self.Point1.y = self.Point1.y * (zc * self.Point1.z + 1)
        self.Point2.x = self.Point2.x * (zc * self.Point2.z + 1)
        self.Point2.y = self.Point2.y * (zc * self.Point2.z + 1)
        m = (self.Point1.x + self.Point2.x) / 2
        n = (self.Point1.y + self.Point2.y) / 2
        k = (self.Point1.z + self.Point2.z) / 2
        s = sin(-pi / 12)
        c = cos(-pi / 12)
        x = self.Point1.x
        y = self.Point1.y
        z = self.Point1.z
        self.Point1.x = c * (x - m) + s * (n - y) + m
        self.Point1.y = s * (x - m) + c * (y - n) + n
        self.Point1.z = z
        x = self.Point2.x
        y = self.Point2.y
        z = self.Point2.z
        self.Point2.x = c * (x - m) + s * (n - y) + m
        self.Point2.y = s * (x - m) + c * (y - n) + n
        self.Point2.z = z
        self.Point1.x = self.Point1.x / (self.Point1.z * zc + 1)
        self.Point1.y = self.Point1.y / (self.Point1.z * zc + 1)
        self.Point2.x = self.Point2.x / (self.Point2.z * zc + 1)
        self.Point2.y = self.Point2.y / (self.Point2.z * zc + 1)
        self.DrawLine()

    def Mirror(self, event):
        if event.char == 'z':
            m = (self.Point1.x + self.Point2.x) / 2
            n = (self.Point1.y + self.Point2.y) / 2
            x = self.Point1.x
            y = self.Point1.y
            self.Point1.x = -1 * x + 2 * m
            self.Point1.y = y
            x = self.Point2.x
            y = self.Point2.y
            self.Point2.x = -1 * x + 2 * m
            self.Point2.y = y
            self.DrawLine()
        if event.char == 'x':
            m = (self.Point1.x + self.Point2.x) / 2
            n = (self.Point1.y + self.Point2.y) / 2
            x = self.Point1.x
            y = self.Point1.y
            self.Point1.x = x
            self.Point1.y = y * (-1) + 2 * n
            x = self.Point2.x
            y = self.Point2.y
            self.Point2.x = x
            self.Point2.y = y * (-1) + 2 * n
            self.DrawLine()

    def Scale(self, event):
        if event.char == 'q':
            m = (self.Point1.x + self.Point2.x) / 2
            n = (self.Point1.y + self.Point2.y) / 2
            a = 1.1
            x = self.Point1.x
            y = self.Point1.y
            self.Point1.x = x * a + (-1) * m * a + m
            self.Point1.y = y * a + (-1) * n * a + n
            x = self.Point2.x
            y = self.Point2.y
            self.Point2.x = x * a + (-1) * m * a + m
            self.Point2.y = y * a + (-1) * n * a + n
            self.DrawLine()
        if event.char == 'w':
            m = (self.Point1.x + self.Point2.x) / 2
            n = (self.Point1.y + self.Point2.y) / 2
            a = 0.9
            x = self.Point1.x
            y = self.Point1.y
            self.Point1.x = x * a + (-1) * m * a + m
            self.Point1.y = y * a + (-1) * n * a + n
            x = self.Point2.x
            y = self.Point2.y
            self.Point2.x = x * a + (-1) * m * a + m
            self.Point2.y = y * a + (-1) * n * a + n
            self.DrawLine()


def hightlight(event):
    for i in range(len(lines)):
        if lines[i].Fit(event):
            index[0] = 1
            index[1] = i
            lines[i].High = True
            can.itemconfig(lines[i].idLine, fill='red')
            can.itemconfig(lines[i].idLeft, fill='red')
            can.itemconfig(lines[i].idRight, fill='red')
            higlighter(lines[i])
            return
    for j in range(len(Figures)):
        if Figures[j].FitFig(event):
            index[0] = 2
            index[1] = j
            Figures[j].High = True
            Figures[j].RedLy()
            return
    for j in range(len(Triangles)):
        if Triangles[j].FitTri(event):
            index[0] = 3
            index[1] = j
            Triangles[j].High = True
            Triangles[j].RedLy()
            return

    for l in range(len(lines)):
        lines[l].High = False
        can.itemconfig(lines[l].idLine, fill=_from_rgb((lines[l].r, lines[l].g, lines[l].b)))
        can.itemconfig(lines[l].idLeft, fill=_from_rgb((lines[l].r, lines[l].g, lines[l].b)))
        can.itemconfig(lines[l].idRight, fill=_from_rgb((lines[l].r, lines[l].g, lines[l].b)))
    for m in range(len(Triangles)):
        Triangles[m].High = False
        Triangles[m].Blackly()
    for m in range(len(Figures)):
        Figures[m].High = False
        Figures[m].Blackly()
    if len(MLines) != 0:
        Figures.append(Figure(MLines))
        MLines.clear()
    # for i in old:
    #    can.delete(i.id)
    # old.clear()
    index[0] = 0
    index[1] = 0


def CreateNewLine():
    x1 = width - width / 4 + 50
    y1 = (height + (height - height / 3)) / 2
    x2 = width - 50
    y2 = (height + (height - height / 3)) / 2
    z1 = 0
    z2 = 0
    P1 = Point3D(x1, y1, z1)
    P2 = Point3D(x2, y2, z2)
    line = Line(P1, P2)
    lines.append(line)
    # (y1-y2)x+(x2-x1)y+(x1*y2-x2*y1)=0 - уравнение прямой лежащей на двух точках


def Rotate(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].Rotate(event)
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateFig(event)
    if index[0] == 3:
        ind = index[1]
        if Triangles[ind].High:
            Triangles[ind].RotateTri(event)


def move_line(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].Move(event)
    if index[0] == 2:
        ind = index[1]
        if Figures[ind].High:
            Figures[ind].MoveFig(event)
    if index[0] == 3:
        ind = index[1]
        if Triangles[ind].High:
            Triangles[ind].MoveTri(event)


def mirror(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].Mirror(event)
    if index[0] == 2:
        ind = index[1]
        Figures[ind].MirrorFig(event)
    if index[0] == 3:
        ind = index[1]
        if Triangles[ind].High:
            Triangles[ind].MirrorTri(event)


def scale(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].Scale(event)
    if index[0] == 2:
        ind = index[1]
        Figures[ind].ScaleFig(event)
    if index[0] == 3:
        ind = index[1]
        if Triangles[ind].High:
            Triangles[ind].ScaleTri(event)


def UnionFunk():
    buf = []
    for i in range(len(lines)):
        if lines[i].High:
            can.itemconfig(lines[i].idLine, fill='black')
            can.itemconfig(lines[i].idLeft, fill='black')
            can.itemconfig(lines[i].idRight, fill='black')
            lines[i].High = False
            buf.append(lines[i])
    if len(buf) <= 1:
        return
    else:
        for j in range(len(buf)):
            lines.remove(buf[j])
        Figures.append(Figure(buf))
        buf.clear()


def DisUnionFunk():
    if index[0] == 2:
        ind = index[1]
        for i in range(len(Figures[ind].Lines)):
            lines.append(Figures[ind].Lines[i])
        Figures[ind].High = False
        Figures[ind].Blackly()
        index[0] = 0
        index[1] = 0
        Figures.remove(Figures[ind])


def DeleteFunk():
    if index[0] == 1:
        ind = index[1]
        can.delete(lines[ind].idLine, lines[ind].idLeft, lines[ind].idRight)
        lines.remove(lines[ind])
        index[0] = 0
        index[1] = 0
    if index[0] == 2:
        ind = index[1]
        for i in range(len(Figures[ind].Lines)):
            can.delete(Figures[ind].Lines[i].idLine, Figures[ind].Lines[i].idLeft, Figures[ind].Lines[i].idRight)
        Figures.remove(Figures[ind])
        index[0] = 0
        index[1] = 0


def ReBuildFunk():
    if index[0] == 1:
        ind = index[1]
        lines[ind].Point1.z = float(Entz1.get())
        lines[ind].Point2.z = float(Entz2.get())
        lines[ind].oldz1 = float(Entz1.get())
        lines[ind].oldz2 = float(Entz2.get())
        if float(Entz1.get()) > 0 or float(Entz1.get()) > 0:
            lines[ind].Point1.x = float(Entx1.get()) / (float(Entz1.get()) * zc + 1)
            lines[ind].Point2.x = float(Entx2.get()) / (float(Entz2.get()) * zc + 1)
            lines[ind].Point1.y = float(Enty1.get()) / (float(Entz1.get()) * zc + 1)
            lines[ind].Point2.y = float(Enty2.get()) / (float(Entz2.get()) * zc + 1)
        else:
            lines[ind].Point1.x = float(Entx1.get())
            lines[ind].Point2.x = float(Entx2.get())
            lines[ind].Point1.y = float(Enty1.get())
            lines[ind].Point2.y = float(Enty2.get())
        lines[ind].DrawLine()


def RotateXUp(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].RotateXup()
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateXUp()


def RotateXDw(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].RotateXdwn()
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateXdwn()


def RotateYR(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].RotateYR()
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateYR()


def RotateYL(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].RotateYL()
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateYL()


def RotateZL(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].RotateZL()
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateZL()


def RotateZR(event):
    if index[0] == 1:
        ind = index[1]
        lines[ind].RotateZR()
    if index[0] == 2:
        ind = index[1]
        Figures[ind].RotateZR()


arrpoint = []

MLines = []


def Morphing(self):
    for i in range(len(MLines)):
        can.delete(MLines[i].idLine)
        can.delete(MLines[i].idRight)
        can.delete(MLines[i].idLeft)
    MLines.clear()
    schet = []
    for i in range(len(Figures)):
        if Figures[i].High:
            schet.append(Figures[i])
    for i in range(len(schet[0].Lines)):
        try:
            r = (schet[0].Lines[i].r * (10 - int(Morph.get())) + schet[1].Lines[i].r * int(Morph.get() - 1)) // 9
            g = (schet[0].Lines[i].g * (10 - int(Morph.get())) + schet[1].Lines[i].g * int(Morph.get() - 1)) // 9
            b = (schet[0].Lines[i].b * (10 - int(Morph.get())) + schet[1].Lines[i].b * int(Morph.get() - 1)) // 9
            x1 = (schet[0].Lines[i].Point1.x * (10 - int(Morph.get())) + schet[1].Lines[i].Point1.x * int(
                Morph.get() - 1)) / 9
            x2 = (schet[0].Lines[i].Point2.x * (10 - int(Morph.get())) + schet[1].Lines[i].Point2.x * int(
                Morph.get() - 1)) / 9
            y1 = (schet[0].Lines[i].Point1.y * (10 - int(Morph.get())) + schet[1].Lines[i].Point1.y * int(
                Morph.get() - 1)) / 9
            y2 = (schet[0].Lines[i].Point2.y * (10 - int(Morph.get())) + schet[1].Lines[i].Point2.y * int(
                Morph.get() - 1)) / 9
            P1 = Point3D(x1, y1, 0)
            P2 = Point3D(x2, y2, 0)
            MLines.append(Line(P1, P2))
            MLines[len(MLines) - 1].r = r
            MLines[len(MLines) - 1].g = g
            MLines[len(MLines) - 1].b = b
            MLines[len(MLines) - 1].DrawLine()
        except:
            pass


cord = False
ids = []


def coord(event):
    global cord
    if cord:
        for i in ids:
            can.delete(i)
        ids.clear()
        cord = False
    else:
        ids.append(can.create_line(0, 30, width - width / 4 - 5, 30, fill='black'))
        ids.append(can.create_line(width - width / 4 - 5, 30, width - width / 4 - 25, 20, fill='black'))
        ids.append(can.create_line(width - width / 4 - 5, 30, width - width / 4 - 25, 40, fill='black'))
        ids.append(can.create_line(15, height - 15, 5, height - 35, fill='black'))
        ids.append(can.create_line(15, height - 15, 25, height - 35, fill='black'))
        ids.append(can.create_line(15, 25, 15, height - 15, fill='black'))
        cord = True


def menu(event):
    global xm, ym
    xm = event.x
    ym = event.y
    men.post(xm, ym)


def color():
    cmen.post(xm, ym)


def fat():
    fmen.post(xm, ym)


def f1():
    if index[0] == 1:
        ind = index[1]
        can.itemconfig(lines[ind].idLine, width=1)
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            can.itemconfig(i.idLine, width=1)
            i.DrawLine()


def f2():
    if index[0] == 1:
        ind = index[1]
        can.itemconfig(lines[ind].idLine, width=2)
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            can.itemconfig(i.idLine, width=2)
            i.DrawLine()


def f3():
    if index[0] == 1:
        ind = index[1]
        can.itemconfig(lines[ind].idLine, width=3)
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            can.itemconfig(i.idLine, width=3)
            i.DrawLine()


def f4():
    if index[0] == 1:
        ind = index[1]
        can.itemconfig(lines[ind].idLine, width=4)
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            can.itemconfig(i.idLine, width=4)
            i.DrawLine()


def f5():
    if index[0] == 1:
        ind = index[1]
        can.itemconfig(lines[ind].idLine, width=5)
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            can.itemconfig(i.idLine, width=5)
            i.DrawLine()


def f6():
    if index[0] == 1:
        ind = index[1]
        can.itemconfig(lines[ind].idLine, width=6)
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            can.itemconfig(i.idLine, width=6)
            i.DrawLine()


# _from_rgb((self.r, self.g, self.b))

def yellow():
    if index[0] == 1:
        ind = index[1]
        lines[ind].r = 225
        lines[ind].g = 225
        lines[ind].b = 0
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.r = 255
            i.g = 255
            i.b = 0
            i.DrawLine()


def green():
    if index[0] == 1:
        ind = index[1]
        lines[ind].r = 0
        lines[ind].g = 225
        lines[ind].b = 0
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.r = 0
            i.g = 255
            i.b = 0
            i.DrawLine()


def blue():
    if index[0] == 1:
        ind = index[1]
        lines[ind].r = 0
        lines[ind].g = 0
        lines[ind].b = 255
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.r = 0
            i.g = 0
            i.b = 255
            i.DrawLine()


def black():
    if index[0] == 1:
        ind = index[1]
        lines[ind].r = 0
        lines[ind].g = 0
        lines[ind].b = 0
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.r = 0
            i.g = 0
            i.b = 0
            i.DrawLine()


def clear():
    for i in lines:
        can.delete(i.idLine)
        can.delete(i.idRight)
        can.delete(i.idLeft)
    lines.clear()
    for i in Figures:
        for j in i.Lines:
            can.delete(j.idLine)
            can.delete(j.idRight)
            can.delete(j.idLeft)
    Figures.clear()
    # for i in old:
    # can.delete(i.id)


class Tri:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.id = can.create_polygon(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, fill='white',
                                     outline='black')


global old


def Land():
    new = []
    old = []
    old.append(Tri(450, 225, 250, 425, 650, 425))
    for i in range(6):
        for j in range(len(old)):
            new.append(Tri(old[j].x1, old[j].y1, (old[j].x1 + old[j].x2) / 2, (old[j].y1 + old[j].y2) / 2 - 10,
                           (old[j].x1 + old[j].x3) / 2, (old[j].y1 + old[j].y3) / 2 - rand.randint(10, 30)))
            new.append(
                Tri((old[j].x1 + old[j].x2) / 2, (old[j].y1 + old[j].y2) / 2 - 10, (old[j].x1 + old[j].x3) / 2,
                    (old[j].y1 + old[j].y3) / 2 - 10, (old[j].x3 + old[j].x2) / 2,
                    (old[j].y3 + old[j].y2) / 2 - rand.randint(10, 30)))
            new.append(Tri(old[j].x2, old[j].y2, (old[j].x1 + old[j].x2) / 2, (old[j].y1 + old[j].y2) / 2 - 10,
                           (old[j].x3 + old[j].x2) / 2, (old[j].y3 + old[j].y2) / 2 - rand.randint(10, 30)))
            new.append(Tri(old[j].x3, old[j].y3, (old[j].x1 + old[j].x3) / 2, (old[j].y1 + old[j].y3) / 2 - 10,
                           (old[j].x3 + old[j].x2) / 2, (old[j].y3 + old[j].y2) / 2 - rand.randint(10, 30)))
            can.update()

        for j in old:
            can.delete(j.id)
        old = new.copy()
        new.clear()


class Triangle:
    High = False

    def __init__(self, P1, P2, P3, P4, P5, P6):
        self.Med = []
        self.Bis = []
        self.Vis = []
        self.Lines = []
        self.Lines.append(Line(P1, P2))
        self.Lines.append(Line(P3, P4))
        self.Lines.append(Line(P5, P6))
        mid1 = Point3D((self.Lines[0].Point1.x + self.Lines[0].Point2.x) / 2,
                       (self.Lines[0].Point1.y + self.Lines[0].Point2.y) / 2, 0)
        mid2 = Point3D((self.Lines[1].Point1.x + self.Lines[1].Point2.x) / 2,
                       (self.Lines[1].Point1.y + self.Lines[1].Point2.y) / 2, 0)
        mid3 = Point3D((self.Lines[2].Point1.x + self.Lines[1].Point2.x) / 2,
                       (self.Lines[2].Point1.y + self.Lines[2].Point2.y) / 2, 0)
        self.Med.append(Line(P4.Copy(), mid1))
        self.Med.append(Line(P1.Copy(), mid2))
        self.Med.append(Line(P2.Copy(), mid3))
        # A = (P2.x - P1.x) / sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2) + (P4.x - P1.x) / sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2)
        # B = (P2.y - P1.y) / sqrt((P2.x - P1.x) ** 2 + (P2.y - P1.y) ** 2) + (P4.y - P1.y) / sqrt(
        #    (P4.x - P1.x) ** 2 + (P4.y - P1.y) ** 2)
        # x = (B*(P2.y*P4.y-P2.x*P4.y))/(B*(P2.y-P4.y)-A*(P4.x-P2.x))
        # y = -A*x/B
        # A1 = P2.y - P4.y
        # B1 = P4.x - P2.x
        # C1 = P2.x * P4.y - P4.x * P2.y
        # if B1 == 0:
        #    B1 = 1
        # x = (A1 * C1 + A1 * B1 * P1.y - B1 * P1.x)/(-(A1**2)-(B1**2))
        # y = (-A1*x-C1)/B1
        # self.Vis.append(Line(P1.Copy(), Point3D(x, y, 0)))

    def DrawTri(self):
        for i in self.Med:
            can.delete(i.idLine)
            can.delete(i.idLeft)
            can.delete(i.idRight)
        self.Med.clear()
        mid1 = Point3D((self.Lines[0].Point1.x + self.Lines[0].Point2.x) / 2,
                       (self.Lines[0].Point1.y + self.Lines[0].Point2.y) / 2, 0)
        mid2 = Point3D((self.Lines[1].Point1.x + self.Lines[1].Point2.x) / 2,
                       (self.Lines[1].Point1.y + self.Lines[1].Point2.y) / 2, 0)
        mid3 = Point3D((self.Lines[2].Point1.x + self.Lines[1].Point2.x) / 2,
                       (self.Lines[2].Point1.y + self.Lines[2].Point2.y) / 2, 0)
        self.Med.append(Line(self.Lines[1].Point2.Copy(), mid1))
        self.Med.append(Line(self.Lines[0].Point1.Copy(), mid2))
        self.Med.append(Line(self.Lines[0].Point2.Copy(), mid3))
        for i in self.Vis:
            can.delete(i.idLine)
            can.delete(i.idLeft)
            can.delete(i.idRight)
        self.Vis.clear()
        # A = (P2.x - P1.x)/sqrt()
        # A1 = self.Lines[0].Point2.y - self.Lines[1].Point2.y
        # B1 = self.Lines[1].Point2.x - self.Lines[0].Point2.x
        # C1 = self.Lines[0].Point2.x * self.Lines[1].Point2.y - self.Lines[1].Point2.x * self.Lines[0].Point2.y
        # B2 = ((A1 * self.Lines[0].Point1.y - B1 * self.Lines[0].Point1.x) / A1)
        # A2 = (-1) * B1 * B2 / A1
        # x = (A1 * C1 + A1 * B1 * self.Lines[0].Point1.y - B1 * self.Lines[0].Point1.x) / (-(A1 ** 2) - (B1 ** 2))
        # y = (-A1 * x - C1) / B1
        # self.Vis.append(Line(self.Lines[0].Point1.Copy(), Point3D(x, y, 0)))
        for i in self.Lines:
            i.DrawLine()

    def FitTri(self, event):
        for i in range(len(self.Lines)):
            if self.Lines[i].Fit(event):
                return True
        return False

    def RedLy(self):
        for i in range(len(self.Lines)):
            can.itemconfig(self.Lines[i].idLine, fill='red')
            can.itemconfig(self.Lines[i].idLeft, fill='red')
            can.itemconfig(self.Lines[i].idRight, fill='red')

    def Blackly(self):
        for i in range(len(self.Lines)):
            can.itemconfig(self.Lines[i].idLine, fill=_from_rgb((self.Lines[i].r, self.Lines[i].g, self.Lines[i].b)))
            can.itemconfig(self.Lines[i].idLeft, fill=_from_rgb((self.Lines[i].r, self.Lines[i].g, self.Lines[i].b)))
            can.itemconfig(self.Lines[i].idRight, fill=_from_rgb((self.Lines[i].r, self.Lines[i].g, self.Lines[i].b)))

    def X0(self):
        x0 = 0
        for i in range(len(self.Lines)):
            x0 += self.Lines[i].Point1.x + self.Lines[i].Point2.x
        return x0 / (len(self.Lines) * 2)

    def Y0(self):
        y0 = 0
        for i in range(len(self.Lines)):
            y0 += self.Lines[i].Point1.y + self.Lines[i].Point2.y
        return y0 / (len(self.Lines) * 2)

    def Z0(self):
        z0 = 0
        for i in range(len(self.Lines)):
            z0 += self.Lines[i].Point1.z + self.Lines[i].Point2.z
        return z0 / (len(self.Lines) * 2)

    def MoveTri(self, event):
        m = self.X0()
        n = self.Y0()
        ok = False
        for i in range(len(self.Lines)):
            if self.Lines[i].FitRes(event):
                self.Lines[i].Resize(event)
                ok = True
        if ok:
            self.DrawTri()
            return
        for i in range(len(self.Lines)):
            x = self.Lines[i].Point1.x
            y = self.Lines[i].Point1.y
            self.Lines[i].Point1.x = x + event.x - m
            self.Lines[i].Point1.y = y + event.y - n
            x = self.Lines[i].Point2.x
            y = self.Lines[i].Point2.y
            self.Lines[i].Point2.x = x + event.x - m
            self.Lines[i].Point2.y = y + event.y - n
        self.DrawTri()

    def RotateTri(self, event):
        m = self.X0()
        n = self.Y0()
        for i in range(len(self.Lines)):
            if event.delta > 0:
                s = sin(pi / 12)
                c = cos(pi / 12)
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point1.y = c * (y - n) + s * (x - m) + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point2.y = c * (y - n) + s * (x - m) + n
            else:
                s = sin(-pi / 12)
                c = cos(-pi / 12)
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point1.y = c * (y - n) + s * (x - m) + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = c * (x - m) + s * (n - y) + m
                self.Lines[i].Point2.y = c * (y - n) + s * (x - m) + n
        self.DrawTri()

    def MirrorTri(self, event):
        m = self.X0()
        n = self.Y0()
        if event.char == 'z':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * (-1) + 2 * m
                self.Lines[i].Point1.y = y
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * (-1) + 2 * m
                self.Lines[i].Point2.y = y
        if event.char == 'x':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x
                self.Lines[i].Point1.y = y * (-1) + 2 * n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x
                self.Lines[i].Point2.y = y * (-1) + 2 * n
        self.DrawTri()

    def ScaleTri(self, event):
        m = self.X0()
        n = self.Y0()
        if event.char == 'q':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * 1.1 - m * 1.1 + m
                self.Lines[i].Point1.y = y * 1.1 - n * 1.1 + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * 1.1 - m * 1.1 + m
                self.Lines[i].Point2.y = y * 1.1 - n * 1.1 + n
        if event.char == 'w':
            for i in range(len(self.Lines)):
                x = self.Lines[i].Point1.x
                y = self.Lines[i].Point1.y
                self.Lines[i].Point1.x = x * 0.9 - m * 0.9 + m
                self.Lines[i].Point1.y = y * 0.9 - n * 0.9 + n
                x = self.Lines[i].Point2.x
                y = self.Lines[i].Point2.y
                self.Lines[i].Point2.x = x * 0.9 - m * 0.9 + m
                self.Lines[i].Point2.y = y * 0.9 - n * 0.9 + n
        self.DrawTri()


def CreateObject():
    FigMen.post(308, 58)


def CreateRectangle():
    buf = []
    Point1 = Point3D(500, 500, 0)
    Point12 = Point3D(500, 500, 0)
    Point2 = Point3D(600, 500, 0)
    Point22 = Point3D(600, 500, 0)
    Point3 = Point3D(600, 600, 0)
    Point32 = Point3D(600, 600, 0)
    Point4 = Point3D(500, 600, 0)
    Point42 = Point3D(500, 600, 0)
    buf.append(Line(Point1, Point2))
    buf.append(Line(Point12, Point4))
    buf.append(Line(Point22, Point32))
    buf.append(Line(Point3, Point42))
    Figures.append(Figure(buf))


def CreateTriangle():
    Point1 = Point3D(500, 500, 0)
    Point12 = Point3D(500, 500, 0)
    Point2 = Point3D(600, 500, 0)
    Point22 = Point3D(600, 500, 0)
    Point3 = Point3D(600, 600, 0)
    Point32 = Point3D(600, 600, 0)
    Triangles.append(Triangle(Point1, Point2, Point22, Point32, Point12, Point3))


def Save():
    filename = asksaveasfilename()
    Stream = open(filename, 'w')
    for i in lines:
        Stream.write(str(i.Point1.x) + " " + str(i.Point1.y) + " *\n")
        Stream.write(str(i.Point2.x) + " " + str(i.Point2.y) + " *\n")
        Stream.write("-------------------\n")
    for j in Figures:
        for i in j.Lines:
            Stream.write(str(i.Point1.x) + " " + str(i.Point1.y) + " *\n")
            Stream.write(str(i.Point2.x) + " " + str(i.Point2.y) + " *\n")
        Stream.write("-------------------\n")
    for j in Triangles:
        for i in j.Lines:
            Stream.write(str(i.Point1.x) + " " + str(i.Point1.y) + " *\n")
            Stream.write(str(i.Point2.x) + " " + str(i.Point2.y) + " *\n")
        Stream.write("-------------------\n")
    Stream.close()


def Download():
    filename = askopenfilename()
    # clear()
    Stream = open(filename, 'r')
    buf = []
    for i in Stream:
        if i[0] != '-':
            k = 0
            buff = ""
            while i[k] != '*':
                if i[k] != ' ':
                    buff += str(i[k])
                else:
                    buf.append(float(buff))
                    buff = ""
                k += 1
        else:
            if len(buf) == 0:
                pass
            if len(buf) == 4:
                lines.append(Line(Point3D(buf[0], buf[1], 0), Point3D(buf[2], buf[3], 0)))
            if len(buf) > 4:
                buffer = []
                j = 0
                while j < len(buf) - 3:
                    buffer.append(Line(Point3D(buf[j], buf[j + 1], 0), Point3D(buf[j + 2], buf[j + 3], 0)))
                    j += 4
                Figures.append(Figure(buffer))
                buffer = []
            buf = []
    Stream.close()


def ReR(self):
    if index[0] == 1:
        ind = index[1]
        lines[ind].r = R.get()
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.r = R.get()
            i.DrawLine()


def ReG(self):
    if index[0] == 1:
        ind = index[1]
        lines[ind].g = G.get()
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.g = G.get()
            i.DrawLine()


def ReB(self):
    if index[0] == 1:
        ind = index[1]
        lines[ind].b = B.get()
        lines[ind].DrawLine()
    if index[0] == 2:
        ind = index[1]
        for i in Figures[ind].Lines:
            i.b = B.get()
            i.DrawLine()


def Fx(x, x1, x2, y1, y2):
    if x2 - x1 == 0:
        return (-x * (y1 - y2) - (x1 * y2 - x2 * y1)) / ((x2 - x1) + 0.000001)
    return (-x * (y1 - y2) - (x1 * y2 - x2 * y1)) / (x2 - x1)


def SplineFunk():
    if index[0] == 2:
        ind = index[1]
        arr = []
        for i in Figures[ind].Lines:
            arr.append((i.Point1.x, -i.Point1.y))
            arr.append((i.Point2.x, -i.Point2.y))
        ctr = np.array(arr)
        x = ctr[:, 0]
        y = ctr[:, 1]
        l = len(x)
        t = np.linspace(0, 1, l - 2, endpoint=True)
        t = np.append([0, 0, 0], t)
        t = np.append(t, [1, 1, 1])
        tck = [t, [x, y], 3]
        u3 = np.linspace(0, 1, (max(l * 2, 70)), endpoint=True)
        out = interpolate.splev(u3, tck)
        plt.plot(x, y, 'k--', marker='o', markerfacecolor='red')
        plt.plot(out[0], out[1], 'b', linewidth=2.0)
        plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
        plt.show()


def CreateHome():
    w = width / 2
    h = height / 2
    buf = []
    p1 = Point3D(w, h, 5.0)
    p2 = Point3D(w + 120, h, 5.0)
    p3 = Point3D(w + 120, h, 125.0)
    p4 = Point3D(w, h, 125.0)
    p5 = Point3D(w, h - 120, 125.0)
    p6 = Point3D(w + 120, h - 120, 125.0)
    p7 = Point3D(w + 120, h - 120, 5.0)
    p8 = Point3D(w, h - 120, 5.0)
    p9 = Point3D(w + 60, h - 240, 5.0)
    p10 = Point3D(w + 60, h - 240, 125.0)
    buf.append(Line(p1.Copy(), p2.Copy()))
    buf.append(Line(p2.Copy(), p3.Copy()))
    buf.append(Line(p3.Copy(), p4.Copy()))
    buf.append(Line(p1.Copy(), p4.Copy()))
    buf.append(Line(p4.Copy(), p5.Copy()))
    buf.append(Line(p5.Copy(), p6.Copy()))
    buf.append(Line(p6.Copy(), p7.Copy()))
    buf.append(Line(p7.Copy(), p8.Copy()))
    buf.append(Line(p8.Copy(), p5.Copy()))
    buf.append(Line(p1.Copy(), p8.Copy()))
    buf.append(Line(p2.Copy(), p7.Copy()))
    buf.append(Line(p3.Copy(), p6.Copy()))
    buf.append(Line(p5.Copy(), p10.Copy()))
    buf.append(Line(p6.Copy(), p10.Copy()))
    buf.append(Line(p7.Copy(), p9.Copy()))
    buf.append(Line(p8.Copy(), p9.Copy()))
    buf.append(Line(p10.Copy(), p9.Copy()))
    Figures.append(Figure(buf))
    for i in Figures[len(Figures) - 1].Lines:
        i.Point1.x = i.Point1.x / (i.Point1.z * zc + 1)
        i.Point1.y = i.Point1.y / (i.Point1.z * zc + 1)
        i.Point2.x = i.Point2.x / (i.Point2.z * zc + 1)
        i.Point2.y = i.Point2.y / (i.Point2.z * zc + 1)
    Figures[len(Figures) - 1].DrawFig()


def LookFunk(self):
    for i in Figures:
        for j in i.Lines:
            j.Point1.x = j.Point1.x * (abs((Look.get() / 1000) - 1) * j.Point1.z + 1)
            j.Point1.y = j.Point1.y * (abs((Look.get() / 1000) - 1) * j.Point1.z + 1)
            j.Point2.x = j.Point2.x * (abs((Look.get() / 1000) - 1) * j.Point2.z + 1)
            j.Point2.y = j.Point2.y * (abs((Look.get() / 1000) - 1) * j.Point2.z + 1)
            j.Point1.x = j.Point1.x / (((Look.get() / 1000)) * j.Point1.z + 1)
            j.Point1.y = j.Point1.y / (((Look.get() / 1000)) * j.Point1.z + 1)
            j.Point2.x = j.Point2.x / (((Look.get() / 1000)) * j.Point2.z + 1)
            j.Point2.y = j.Point2.y / (((Look.get() / 1000)) * j.Point2.z + 1)
        i.DrawFig()


R.config(command=ReR)
G.config(command=ReG)
B.config(command=ReB)
men = Menu(tearoff=0)
men.add_command(label="Цвет", command=color)
men.add_command(label="Толщина", command=fat)
men.add_command(label="Отчистить", command=clear)
cmen = Menu(tearoff=0)
cmen.add_command(label='Желтый', command=yellow)
cmen.add_command(label='Зеленый', command=green)
cmen.add_command(label='Синий', command=blue)
cmen.add_command(label='Черный', command=black)
fmen = Menu(tearoff=0)
FigMen = Menu(tearoff=0)
Look.config(command=LookFunk)
FigMen.add_command(label='Линия', command=CreateNewLine)
FigMen.add_command(label='Квадрат', command=CreateRectangle)
FigMen.add_command(label='Треугольник', command=CreateTriangle)
FigMen.add_command(label='Домик', command=CreateHome)
fmen.add_command(label="1", command=f1)
fmen.add_command(label="2", command=f2)
fmen.add_command(label="3", command=f3)
fmen.add_command(label="4", command=f4)
fmen.add_command(label="5", command=f5)
fmen.add_command(label="6", command=f6)
can.bind('<Button-3>', menu)
CreateNewLine()
SaveBtn.config(command=Save)
DownLoadBtn.config(command=Download)
ReBuild.config(command=ReBuildFunk)
UnionBtn.config(command=UnionFunk)
AddBtn.config(command=CreateObject)
SplineBtn.config(command=SplineFunk)
DeleteBtn.config(command=DeleteFunk)
window.bind('z', mirror)
window.bind('p', coord)
window.bind('x', mirror)
window.bind('c', mirror)
window.bind('q', scale)
window.bind('w', scale)
window.bind('<Up>', RotateXUp)
window.bind('<Down>', RotateXDw)
window.bind('<Right>', RotateYR)
window.bind('<Left>', RotateYL)
window.bind('[', RotateZL)
window.bind(']', RotateZR)
Morph.config(command=Morphing)
DisUnionBtn.config(command=DisUnionFunk)
can.bind('<Button-1>', hightlight)
can.bind('<B1-Motion>', move_line)
can.bind('<MouseWheel>', Rotate)
window.mainloop()
