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
import tkinter.filedialog
from tkinter import N, E, S, W, TOP, BOTTOM, LEFT, RIGHT, HORIZONTAL, VERTICAL

import mandelbrot

WINDOW_SIZE_MIN = (320, 240)

VERSION = 'v0.0.0'
TITLE = 'Chaos'
AUTHOR = 'Lukas Singer'
LICENSE = 'WTFPL (see COPYING or <http://www.wtfpl.net/>)'
ABOUT_TEXT = """
{title} - A Free  Fractal Generator
written in Python
{version}

Copyright 2016, {author}
{license}

have fun :-)
""".format(title=TITLE, version=VERSION, author=AUTHOR, license=LICENSE)

###############################################################################
###   THE CHAOS BEGINS   ######################################################
###############################################################################

class Chaos:
    def __init__(self):
        super().__init__()

        self.img_id = None
        self.mouse_down_position = None
        self.complex_plane = None

        self.root = tk.Tk()
        self.root.title('{} - {}'.format(TITLE, VERSION))

        self.canvas_size_x = tk.IntVar()
        self.canvas_size_x.set(200)
        self.canvas_size_y = tk.IntVar()
        self.canvas_size_y.set(200)
        self.canvas_lock_ratio = tk.BooleanVar()
        self.canvas_lock_ratio.set(True)

        self.mandelbrot_bailout = tk.DoubleVar()
        self.mandelbrot_bailout.set(2.0)
        self.mandelbrot_max_iter = tk.IntVar()
        self.mandelbrot_max_iter.set(512)
        self.mandelbrot_coloring = tk.StringVar()
        self.mandelbrot_coloring.set('Default')

        self.mandelbrot_colorings = {
            'Default': lambda: None,
            'Modulo 2': lambda: mandelbrot.modulo_coloring((0, 0, 0),
                                                           (255, 0, 0),
                                                           (0, 0, 255)),
            'Modulo 3': lambda: mandelbrot.modulo_coloring((0, 0, 0),
                                                           (255, 0, 0),
                                                           (0, 255, 0),
                                                           (0, 0, 255)),
            'Simple Shading': lambda: mandelbrot.simple_shading(
                (0, 0, 0),
                (16, 16, 16),
                (255, 255, 255),
                self.mandelbrot_max_iter.get())}

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
        self.filemenu.add_command(label='Save', command=lambda:print('sorry'))
        self.filemenu.add_command(label='Eport', command=self.export_image)
#        self.filemenu.add_separator()
        self.filemenu.add_command(label='Close', command=self.root.quit)
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        self.rendermenu = tk.Menu(self.menubar, tearoff=0)
        self.rendermenu.add_command(label='Mandelbrot',
                                    command=self.mandelbrot)
        self.menubar.add_cascade(label='Render', menu=self.rendermenu)

        self.settingsmenu = tk.Menu(self.menubar, tearoff=0)
        self.settingsmenu.add_command(label='Canvas',
                                      command=self.canvas_settings)
        self.settingsmenu.add_command(label='Mandelbrot',
                                      command=self.mandelbrot_settings)
        self.menubar.add_cascade(label='Settings', menu=self.settingsmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About', command=self.about_dialog)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.root.minsize(*WINDOW_SIZE_MIN)

        self.root.mainloop()


    def mandelbrot(self, complex_coords=None):
        # TODO: implement the cursor manager found here:
        #       http://effbot.org/zone/tkinter-busy.htm
        self.root.config(cursor='spraycan')
        if self.img_id:
            self.canvas.delete(self.img_id)
            self.img_id = None
        self.root.update() # show cursor and clear canvas
        if not complex_coords:
            complex_coords = (-2.2+1.4j, 1-1.4j)
        if self.canvas_lock_ratio.get():
            complex_coords = self.expand_complex_coords_to_canvas_size(
                complex_coords)
        print(self.canvas_lock_ratio.get())
        self.complex_plane = mandelbrot.mandelbrot(
            self.canvas_size_x.get(),
            self.canvas_size_y.get(),
            *complex_coords,
            self.mandelbrot_colorings[self.mandelbrot_coloring.get()](),
            self.mandelbrot_bailout.get(),
            self.mandelbrot_max_iter.get())
        self.img_id = self.canvas.create_image(
            0, 0,
            anchor=N+W,
            image=self.complex_plane.get_tk_image())
        self.root.config(cursor='')

    def expand_complex_coords_to_canvas_size(self, complex_coords):
        # this function does what it should, but it looks ugly.
        # TODO: make it better.
        z1, z2 = complex_coords
        canvas_w, canvas_h = self.canvas_size_x.get(), self.canvas_size_y.get()
        complex_w, complex_h = abs(z2.real - z1.real), abs(z2.imag - z1.imag)
        pixel_delta_x = complex_w / canvas_w
        pixel_delta_y = complex_h / canvas_h
        if pixel_delta_x < pixel_delta_y:
            expand = canvas_w * pixel_delta_y
            center = z1.real + (z2.real - z1.real) / 2
            z1 = (center - expand / 2) + (z1.imag * 1j)
            z2 = (center + expand / 2) + (z2.imag * 1j)
        if pixel_delta_x > pixel_delta_y:
            expand = canvas_h * pixel_delta_x
            center = z1.imag + (z2.imag - z1.imag) / 2
            z1 = z1.real + ((center - expand / 2) * 1j)
            z2 = z2.real + ((center + expand / 2) * 1j)
        return z1, z2

    def export_image(self):
        if self.complex_plane:
            filename = tk.filedialog.asksaveasfilename(defaultextension='.png')
            if filename:
                img = self.complex_plane.get_pil_image()
                img.save(filename)


    def mouse_down(self, event):
        if self.complex_plane:
            self.root.config(cursor='cross')
            p = (event.x, event.y)
            self.mouse_down_position = self.complex_plane.p2c(p)

    def mouse_up(self, event):
        if self.mouse_down_position and self.complex_plane:
            self.root.config(cursor='')
            p = event.x, event.y
            if p == self.mouse_down_position:
                # we have to do this because of div by zero risk
                p = p[0] + 1, p[1] + 1
            self.canvas.delete(self.img_id)
            complex_coords = (self.mouse_down_position,
                              self.complex_plane.p2c(p))
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

    def canvas_settings(self):
        window = tk.Toplevel()
        window.title('Canvas Settings')
        tk.Label(window, text='Canvas size [W, H]:').grid(
            row=0, column=0, sticky=W)
        tk.Entry(window, textvariable=self.canvas_size_x).grid(
            row=0, column=1, sticky=N+E+S+W)
        tk.Entry(window, textvariable=self.canvas_size_y).grid(
            row=0, column=2, stick=N+E+S+W)
        tk.Label(window, text='Lock ratio:').grid(row=1, column=0, sticky=W)
        tk.Checkbutton(window, text='Enabled',
                       variable=self.canvas_lock_ratio).grid(
                           row=1, column=1, sticky=N+S+W)

    def mandelbrot_settings(self):
        window = tk.Toplevel()
        window.title('Mandelbrot Settings')
        tk.Label(window, text='Bailout:').grid(row=0, column=0, sticky=W)
        tk.Entry(window, textvariable=self.mandelbrot_bailout).grid(
            row=0, column=1)
        tk.Label(window, text='Max. Iterations:').grid(
            row=1, column=0, sticky=W)
        tk.Entry(window, textvariable=self.mandelbrot_max_iter).grid(
            row=1, column=1)
        tk.Label(window, text='Coloring:').grid(row=2, column=0, sticky=W)
        tk.OptionMenu(window, self.mandelbrot_coloring,
                      *self.mandelbrot_colorings.keys()).grid(
                          row=2, column=1, sticky=N+E+S+W)

    def about_dialog(self):
        window = tk.Toplevel()
        window.title('About {title}'.format(TITLE))
        tk.Label(window, text=ABOUT_TEXT).pack(padx=10, pady=5)
        tk.Button(window, text='Ok', command=window.destroy).pack(pady=5)


if __name__ == '__main__':
    Chaos()
