#!/usr/bin/env python
"""
Filename: chaos.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/05/25
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: This is the user interface of a fractal generator.
"""

import tkinter as tk
from tkinter import N, E, S, W, TOP, BOTTOM, LEFT, RIGHT, HORIZONTAL, VERTICAL

import mandelbrot

WINDOW_SIZE_MIN = (320, 240)

class Chaos:
    def __init__(self):
        super().__init__()

        self.img_id = None
        self.mouse_down_position = None
        self.complex_plane = None

        self.root = tk.Tk()
        self.root.title('Chaos')

        self.canvas = tk.Canvas(self.root)
        self.canvas.bind('<Motion>', self.mouse_move)
        self.canvas.bind('<ButtonPress-1>', self.mouse_down)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
        self.canvas.grid(row=0, column=0, sticky=N+E+S+W)

        self.scroll_x = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self.canvas, orient=tk.VERTICAL)
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)
        self.scroll_x.pack(fill=tk.X, side=tk.BOTTOM)
        self.scroll_y.pack(fill=tk.Y, side=tk.RIGHT)

        self.canvas.config(xscrollcommand=self.scroll_x.set)
        self.canvas.config(yscrollcommand=self.scroll_y.set)
        self.canvas.config(scrollregion=(0, 0, 640, 480))

        self.coords_var = tk.StringVar()
        self.coords_var.set('###')
        self.coords_lbl = tk.Label(self.root, textvariable=self.coords_var)
        self.coords_lbl.grid(row=1, column=0, sticky=S+E)

        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Save', command=lambda:print('a'))
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Close', command=self.root.quit)
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        self.fractalmenu = tk.Menu(self.menubar, tearoff=0)
        self.fractalmenu.add_command(
            label='Mandelbrot', command=self.mandelbrot)
        self.menubar.add_cascade(label='Fractal', menu=self.fractalmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About')
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        # set the minimum window size like described here:
        # http://stackoverflow.com/a/10452097/3403216
        self.root.update()
        self.root.minsize(*WINDOW_SIZE_MIN)

        self.root.mainloop()


    def mandelbrot(self, complex_coords=None):
        # TODO: implement the cursor manager found here:
        #       http://effbot.org/zone/tkinter-busy.htm
        self.root.config(cursor='spraycan')
        self.root.update()
        if not complex_coords:
            complex_coords = (-2.2+1.4j, 1-1.4j)
        if self.img_id:
            self.canvas.delete(self.img_id)
            self.img_id = None
        self.complex_plane = mandelbrot.mandelbrot(150, 150, *complex_coords)
        self.img_id = self.canvas.create_image(
            0, 0,
            anchor=N+W,
            image=self.complex_plane.get_tk_image())
        self.root.config(cursor='')


    def mouse_down(self, event):
        if self.complex_plane:
            p = (event.x, event.y)
            self.mouse_down_position = self.complex_plane.p2c(p)

    def mouse_up(self, event):
        if self.mouse_down_position and self.complex_plane:
            self.canvas.delete(self.img_id)
            complex_coords = (self.mouse_down_position,
                              self.complex_plane.p2c((event.x, event.y)))
            self.mandelbrot(complex_coords)
            self.mouse_down_position = None

    def mouse_move(self, event):
        if self.complex_plane:
            x, y = event.x, event.y
            z = self.complex_plane.p2c((x, y))
            self.coords_var.set(
                '({z.real:.5e} + {z.imag:.5e} i)  ({x}, {y})'
                .format(z=z, x=x, y=y))
        else:
            self.coords_var.set('###')



if __name__ == '__main__':
    Chaos()
