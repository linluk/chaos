#!/usr/bin/env python
"""
Filename: coloring_settings.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/06/19
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: This is the UI for the coloring settings.
"""

import tkinter as tk

import tkinter_ex as tke
import settings
import coloring


class ColoringSettings(object):

    def __init__(self, master):
        super().__init__()
        window = tke.Toplevel(master)
        window.title('Coloring Settings')
        self._modulo2(window).grid(row=0, column=0)


    def _modulo2(self, parent):
        frame = tk.Frame(parent)
        tk.Label(frame, text='Modulo 2:').grid(row=0, column=0, sticky=tk.W)
        self._rgb_entries(
            frame,
            'Inner:',
            settings.coloring.get_modulo2_i_r_var(),
            settings.coloring.get_modulo2_i_g_var(),
            settings.coloring.get_modulo2_i_b_var(),
            1, 1)
        self._rgb_entries(
            frame,
            'Rem equals 0:',
            settings.coloring.get_modulo2_0_r_var(),
            settings.coloring.get_modulo2_0_g_var(),
            settings.coloring.get_modulo2_0_b_var(),
            2, 1)
        self._rgb_entries(
            frame,
            'Rem equals 1:',
            settings.coloring.get_modulo2_1_r_var(),
            settings.coloring.get_modulo2_1_g_var(),
            settings.coloring.get_modulo2_1_b_var(),
            3, 1)
        return frame


    def _rgb_entries(self, parent, title, tvr, tvg, tvb, row, start_column):
            tk.Label(parent, text=title).grid(row=row,
                                              column=start_column + 0,
                                              sticky=tk.W)
            tke.IntEntry(
                parent,
                textvariable=tvr,
                maxvalue=255,
                minvalue=0).grid(row=row, column=start_column + 1)
            tke.IntEntry(
                parent,
                textvariable=tvg,
                maxvalue=255,
                minvalue=0).grid(row=row, column=start_column + 2)
            tke.IntEntry(
                parent,
                textvariable=tvb,
                maxvalue=255,
                minvalue=0).grid(row=row, column=start_column + 3)
            b = tk.Button(parent, text='Test')
            def _set_button_color():
                b.config(
                    bg=tke.tk_rgb(tvr.get(), tvg.get(), tvb.get()))
            b.config(command=_set_button_color)
            b.grid(row=row, column=start_column + 4)
            _set_button_color()
