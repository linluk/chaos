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
import settings
import coloring

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
    def __init__(self, parent):
        super().__init__()

        self.last_render_function = None
        self.img_id = None
        self.mouse_down_position = None
        self.complex_plane = None

        self.parent = parent
#        self.root.title('{} - {}'.format(TITLE, VERSION))

        settings.initialize()
        coloring.initialize()

        self.canvas = tk.Canvas(self.parent)
        self.canvas.bind('<Motion>', self.mouse_move)
        self.canvas.bind('<ButtonPress-1>', self.mouse_down)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
        self.canvas.grid(row=0, column=0, sticky=N+E+S+W)

        self.scroll_x = tk.Scrollbar(self.parent, orient=tk.HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self.parent, orient=tk.VERTICAL)
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)
        self.scroll_x.grid(row=1, column=0, sticky=E+W)
        self.scroll_y.grid(row=0, column=1, sticky=N+S)

        self.canvas.config(xscrollcommand=self.scroll_x.set)
        self.canvas.config(yscrollcommand=self.scroll_y.set)

        self.coords_var = tk.StringVar()
        self.coords_var.set('###')
        self.coords_lbl = tk.Label(self.parent, textvariable=self.coords_var)
        self.coords_lbl.grid(row=2, column=0, columnspan=2, sticky=S+E)

        tk.Grid.rowconfigure(self.parent, 0, weight=1)
        tk.Grid.columnconfigure(self.parent, 0, weight=1)

        self.menubar = tke.Menu(self.parent)
        self.parent.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label='Save', command=lambda:print('sorry'))
        self.filemenu.add_command(label='Eport', command=self.export_image)
#        self.filemenu.add_separator()
        self.filemenu.add_command(label='Close', command=self.parent.quit)
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
        self.settingsmenu.add_command(label='Coloring',
                                      command=self.coloring_settings)
        self.menubar.add_cascade(label='Settings', menu=self.settingsmenu)

        self.helpmenu = tke.Menu(self.menubar)
        self.helpmenu.add_command(label='About', command=self.about_dialog)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.parent.minsize(*WINDOW_SIZE_MIN)

        self.parent.mainloop()


    def before_render(self, complex_coords, default_complex_coords):
        # TODO: implement the cursor manager found here:
        #       http://effbot.org/zone/tkinter-busy.htm
        self.parent.config(cursor='spraycan')
        if self.img_id:
            self.canvas.delete(self.img_id)
            self.img_id = None
        self.parent.update()
        if not complex_coords:
            complex_coords = default_complex_coords
        if settings.canvas.lock_ratio:
            complex_coords = self.expand_complex_coords_to_canvas_size(
                complex_coords)
        return complex_coords

    def after_render(self, last_render_function):
        self.img_id = self.canvas.create_image(
            0, 0,
            anchor=N+W,
            image=self.complex_plane.get_tk_image())
        self.canvas.config(
            scrollregion=(0, 0,
                          settings.canvas.size_x,
                          settings.canvas.size_y))
        self.parent.config(cursor='')
        self.last_render_function = last_render_function

    def render_mandelbrot(self, complex_coords=None):
        complex_coords = self.before_render(complex_coords,
                                            MANDELBROT_DEFAULT_COORDS)
        max_iter = settings.mandelbrot.max_iter
        self.complex_plane = mandelbrot.mandelbrot(
            settings.canvas.size_x,
            settings.canvas.size_y,
            *complex_coords,
            coloring.colorings[settings.mandelbrot.coloring](max_iter),
            settings.mandelbrot.bailout,
            max_iter)
        self.after_render(self.render_mandelbrot)

    def render_julia(self, complex_coords=None):
        complex_coords = self.before_render(complex_coords,
                                            JULIA_DEFAULT_COORDS)
        julia_parameter = settings.julia.parameter_real + (
            settings.julia.parameter_imag * 1j)
        max_iter = settings.julia.max_iter
        self.complex_plane = julia.julia(
            settings.canvas.size_x,
            settings.canvas.size_y,
            *complex_coords,
            julia_parameter,
            coloring.colorings[settings.julia.coloring](max_iter),
            settings.julia.bailout,
            max_iter)
#            -0.12+0.75j)
        self.after_render(self.render_julia)

    def expand_complex_coords_to_canvas_size(self, complex_coords):
        # this function does what it should, but it looks ugly.
        # TODO: make it better.
        z1, z2 = complex_coords
        canvas_w, canvas_h = settings.canvas.size_x, settings.canvas.size_y
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
            self.parent.config(cursor='cross')
            p = (event.x, event.y)
            self.mouse_down_position = self.complex_plane.p2c(p)

    def mouse_up(self, event):
        if (self.mouse_down_position
            and self.complex_plane
            and self.last_render_function):
            self.parent.config(cursor='')
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
        window = tke.Toplevel(self.parent)
        window.title('Canvas Settings')
#        window.transient(self.parent)
        window.resizable(width=False, height=False)
        tk.Label(window, text='Canvas size [W, H]:').grid(
            row=0, column=0, sticky=W)
        tke.IntEntry(window,
                     textvariable=settings.canvas.get_size_x_var()).grid(
                         row=0, column=1, sticky=N+E+S+W)
        tke.IntEntry(window,
                     textvariable=settings.canvas.get_size_y_var()).grid(
                         row=0, column=2, stick=N+E+S+W)
        tk.Label(window, text='Lock ratio:').grid(row=1, column=0, sticky=W)
        tk.Checkbutton(window, text='Enabled',
                       variable=settings.canvas.get_lock_ratio_var()).grid(
                           row=1, column=1, sticky=N+S+W)

    def mandelbrot_settings(self):
        window = tke.Toplevel(self.parent)
        window.title('Mandelbrot Settings')
        tk.Label(window, text='Bailout:').grid(row=0, column=0, sticky=W)
        tke.DoubleEntry(
            window,
            textvariable=settings.mandelbrot.get_bailout_var()).grid(
                row=0, column=1)
        tk.Label(window, text='Max. Iterations:').grid(
            row=1, column=0, sticky=W)
        tke.IntEntry(
            window,
            textvariable=settings.mandelbrot.get_max_iter_var()).grid(
                row=1, column=1)
        tk.Label(window, text='Coloring:').grid(row=2, column=0, sticky=W)
        tk.OptionMenu(window, settings.mandelbrot.get_coloring_var(),
                      *coloring.colorings.keys()).grid(
                          row=2, column=1, sticky=N+E+S+W)

    def julia_settings(self):
        window = tke.Toplevel(self.parent)
        window.title('Julia Settings')
        tk.Label(window, text='Parameter:').grid(row=0, column=0, sticky=W)
        tke.DoubleEntry(
            window,
            textvariable=settings.julia.get_parameter_real_var()).grid(
                row=0, column=1)
        tk.Label(window, text=' + ').grid(row=0, column=2)
        tke.DoubleEntry(
            window,
            textvariable=settings.julia.get_parameter_imag_var()).grid(
                row=0, column=3)
        tk.Label(window, text=' i').grid(row=0, column=4)
        tk.Label(window, text='Bailout:').grid(row=1, column=0, sticky=W)
        tke.DoubleEntry(
            window,
            textvariable=settings.julia.get_bailout_var()).grid(
                row=1, column=1)
        tk.Label(window, text='Max. Iterations:').grid(
            row=2, column=0, sticky=W)
        tke.IntEntry(
            window,
            textvariable=settings.julia.get_max_iter_var()).grid(
                row=2, column=1)
        tk.Label(window, text='Coloring:').grid(row=3, column=0, sticky=W)
        tk.OptionMenu(window, settings.julia.get_coloring_var(),
                      *coloring.colorings.keys()).grid(
                          row=3, column=1, sticky=N+E+S+W)


    def coloring_settings(self):
        def _rgb_entries(parent, tvr, tvg, tvb, row, start_column):
            print(tvr.get())
            print(tvg.get())
            print(tvb.get())
            tke.IntEntry(
                parent,
                textvariable=tvr).grid(row=row, column=start_column + 0)
            tke.IntEntry(
                parent,
                textvariable=tvg).grid(row=row, column=start_column + 1)
            tke.IntEntry(
                parent,
                textvariable=tvb).grid(row=row, column=start_column + 2)

        window = tke.Toplevel(self.parent)
        window.title('Coloring Settings')
        tk.Label(window, text='Modulo 2:').grid(row=0, column=0, sticky=W)
        _rgb_entries(
            window,
            settings.coloring.get_modulo2_i_r_var(),
            settings.coloring.get_modulo2_i_g_var(),
            settings.coloring.get_modulo2_i_b_var(),
            0, 1)


    def about_dialog(self):
        window = tke.Toplevel(self.parent)
        window.title('About {title}'.format(title=TITLE))
        tk.Label(window, text=ABOUT_TEXT).pack(padx=10, pady=5)
        tk.Button(window, text='Ok', command=window.destroy).pack(pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    Chaos(root)
