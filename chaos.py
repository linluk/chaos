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

import tkinter_ex as tke
import mandelbrot
import julia


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

WINDOW_SIZE_MIN = (320, 240)
MANDELBROT_DEFAULT_COORDS = (-2.2+1.4j, 1-1.4j)
JULIA_DEFAULT_COORDS = (-2+2j, 2-2j)

###############################################################################
###   THE CHAOS BEGINS   ######################################################
###############################################################################

class Chaos:
    def __init__(self):
        super().__init__()

        self.last_render_function = None
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

        self.julia_parameter_real = tk.DoubleVar()
        self.julia_parameter_real.set(-0.12)
        self.julia_parameter_imag = tk.DoubleVar()
        self.julia_parameter_imag.set(0.75)

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

        self.scroll_x = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)
#        self.scroll_x.pack(fill=tk.X, side=tk.BOTTOM)
        self.scroll_x.grid(row=1, column=0, sticky=E+W)
#        self.scroll_y.pack(fill=tk.Y, side=tk.RIGHT)
        self.scroll_y.grid(row=0, column=1, sticky=N+S)

        self.canvas.config(xscrollcommand=self.scroll_x.set)
        self.canvas.config(yscrollcommand=self.scroll_y.set)
        self.canvas.config(scrollregion=(0, 0, 640, 480))

        self.coords_var = tk.StringVar()
        self.coords_var.set('###')
        self.coords_lbl = tk.Label(self.root, textvariable=self.coords_var)
        self.coords_lbl.grid(row=2, column=0, columnspan=2, sticky=S+E)

        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)

        self.menubar = tke.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label='Save', command=lambda:print('sorry'))
        self.filemenu.add_command(label='Eport', command=self.export_image)
#        self.filemenu.add_separator()
        self.filemenu.add_command(label='Close', command=self.root.quit)
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        self.rendermenu = tke.Menu(self.menubar)
        self.rendermenu.add_command(label='Mandelbrot',
                                    command=self.render_mandelbrot)
        self.rendermenu.add_command(label='Julia',
                                    command=self.render_julia)
        self.menubar.add_cascade(label='Render', menu=self.rendermenu)

        self.settingsmenu = tke.Menu(self.menubar)
        self.settingsmenu.add_command(label='Canvas',
                                      command=self.canvas_settings)
        self.settingsmenu.add_command(label='Mandelbrot',
                                      command=self.mandelbrot_settings)
        self.settingsmenu.add_command(label='Julia',
                                      command=self.julia_settings)
        self.menubar.add_cascade(label='Settings', menu=self.settingsmenu)

        self.helpmenu = tke.Menu(self.menubar)
        self.helpmenu.add_command(label='About', command=self.about_dialog)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.root.minsize(*WINDOW_SIZE_MIN)

        self.root.mainloop()


    def before_render(self, complex_coords, default_complex_coords):
        # TODO: implement the cursor manager found here:
        #       http://effbot.org/zone/tkinter-busy.htm
        self.root.config(cursor='spraycan')
        if self.img_id:
            self.canvas.delete(self.img_id)
            self.img_id = None
        self.root.update()
        if not complex_coords:
            complex_coords = default_complex_coords
        if self.canvas_lock_ratio.get():
            complex_coords = self.expand_complex_coords_to_canvas_size(
                complex_coords)
        return complex_coords

    def after_render(self, last_render_function):
        self.img_id = self.canvas.create_image(
            0, 0,
            anchor=N+W,
            image=self.complex_plane.get_tk_image())
        self.root.config(cursor='')
        self.last_render_function = last_render_function

    def render_mandelbrot(self, complex_coords=None):
        complex_coords = self.before_render(complex_coords,
                                            MANDELBROT_DEFAULT_COORDS)
        self.complex_plane = mandelbrot.mandelbrot(
            self.canvas_size_x.get(),
            self.canvas_size_y.get(),
            *complex_coords,
            self.mandelbrot_colorings[self.mandelbrot_coloring.get()](),
            self.mandelbrot_bailout.get(),
            self.mandelbrot_max_iter.get())
        self.after_render(self.render_mandelbrot)

    def render_julia(self, complex_coords=None):
        complex_coords = self.before_render(complex_coords,
                                            JULIA_DEFAULT_COORDS)
        julia_parameter = self.julia_parameter_real.get() + (
            self.julia_parameter_imag.get() * 1j)
        self.complex_plane = julia.julia(
            self.canvas_size_x.get(),
            self.canvas_size_y.get(),
            *complex_coords,
            julia_parameter)
#            -0.12+0.75j)
        self.after_render(self.render_julia)

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
        if (self.mouse_down_position
            and self.complex_plane
            and self.last_render_function):
            self.root.config(cursor='')
            p = event.x, event.y
            if p == self.mouse_down_position:
                # we have to do this because of div by zero risk
                p = p[0] + 1, p[1] + 1
            self.canvas.delete(self.img_id)
            complex_coords = (self.mouse_down_position,
                              self.complex_plane.p2c(p))
            self.last_render_function(complex_coords)
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
        window = tke.Toplevel(self.root)
        window.title('Canvas Settings')
#        window.transient(self.root)
        window.resizable(width=False, height=False)
        tk.Label(window, text='Canvas size [W, H]:').grid(
            row=0, column=0, sticky=W)
        tke.IntEntry(window, textvariable=self.canvas_size_x).grid(
            row=0, column=1, sticky=N+E+S+W)
        tke.IntEntry(window, textvariable=self.canvas_size_y).grid(
            row=0, column=2, stick=N+E+S+W)
        tk.Label(window, text='Lock ratio:').grid(row=1, column=0, sticky=W)
        tk.Checkbutton(window, text='Enabled',
                       variable=self.canvas_lock_ratio).grid(
                           row=1, column=1, sticky=N+S+W)

    def mandelbrot_settings(self):
        window = tke.Toplevel(self.root)
        window.title('Mandelbrot Settings')
        tk.Label(window, text='Bailout:').grid(row=0, column=0, sticky=W)
        tke.DoubleEntry(window, textvariable=self.mandelbrot_bailout).grid(
            row=0, column=1)
        tk.Label(window, text='Max. Iterations:').grid(
            row=1, column=0, sticky=W)
        tke.IntEntry(window, textvariable=self.mandelbrot_max_iter).grid(
            row=1, column=1)
        tk.Label(window, text='Coloring:').grid(row=2, column=0, sticky=W)
        tk.OptionMenu(window, self.mandelbrot_coloring,
                      *self.mandelbrot_colorings.keys()).grid(
                          row=2, column=1, sticky=N+E+S+W)

    def julia_settings(self):
        window = tke.Toplevel(self.root)
        window.title('Julia Settings')
        tk.Label(window, text='Parameter:').grid(row=0, column=0, sticky=W)
        tke.DoubleEntry(window, textvariable=self.julia_parameter_real).grid(
            row=0, column=1)
        tk.Label(window, text=' + ').grid(row=0, column=2)
        tke.DoubleEntry(window, textvariable=self.julia_parameter_imag).grid(
            row=0, column=3)
        tk.Label(window, text=' i').grid(row=0, column=4)

    def about_dialog(self):
        window = tke.Toplevel(self.root)
        window.title('About {title}'.format(title=TITLE))
        tk.Label(window, text=ABOUT_TEXT).pack(padx=10, pady=5)
        tk.Button(window, text='Ok', command=window.destroy).pack(pady=5)


if __name__ == '__main__':
    Chaos()
