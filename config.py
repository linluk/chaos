#!/usr/bin/env python
"""
Filename: config.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/06/08
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: Here are all the settings the user can edit.
"""

import tkinter as tk

import tkinter_ex as tke


canvas = None
mandelbrot = None
julia = None


def _add_var_getter_property(cls, attr):
    """ this function is used in the settings_class decorator to add a
    getter for the tk-stringvar and a read/write property to the class.
    cls:  is the class where the attributes are added.
    attr: is the name of the property and for the get_XYZ_var() method.
    """
    field = '_' + attr
    setattr(cls, 'get_{}_var'.format(attr), lambda self: getattr(self, field))
    setattr(cls, attr,
            property(lambda self: getattr(self, field).get(),
                     lambda self, value: getattr(self, field).set(value)))

def settings_class(cls):
    """ this is the decorator function for SettingsBase subclasses.
    it adds getters for the tk-stringvars and properties. it reads the
    names described in the class-variable _SETTINGS.
    """
    for name in cls._SETTINGS:
        _add_var_getter_property(cls, name)
    return cls


class SettingsBase:
    """ this is the base class for a settings class. it automatically
    adds fields to the class described in the class variable _SETTINGS.
    when you subclass SettingsBase you should overwrite _SETTINGS.
    a minimal example could look like this:

      @settings_class
      class MySettings(SettingsBase):
          _SETTINGS = {
              'x': 42,
              'y': 23}

    this would result in a class with a _x tk-intvar and a _y tk-doublevar
    field with the getters get_x_var() and get_y_var() and the properties
    x and y.
    """

    _SETTINGS = {}

    def __init__(self, **kwargs):
        """ creates the fields described in _SETTINGS and initialize
        eighter from the kwargs or from the default values
        """
        super().__init__()
        fields = self._SETTINGS.copy()
        if kwargs:
            for key in kwargs:
                if key in fields:
                    typ = type(fields[key])
                    fields[key] = typ(kwargs[key])
                else:
                    raise KeyError(key)
        for key in fields:
            value = fields[key]
            typ = type(value)
            name = '_' + key
            if typ is int:
                setattr(self, name, tke.IntVar(value))
            elif typ is str:
                setattr(self, name, tke.StringVar(value))
            elif typ is bool:
                setattr(self, name, tke.BooleanVar(value))
            elif typ is float:
                setattr(self, name, tke.DoubleVar(value))
            else:
                raise TypeError(typ)


@settings_class
class _Canvas(SettingsBase):

    _SETTINGS = {
        'size_x': 320,
        'size_y': 240,
        'lock_ratio': True
        }


@settings_class
class _Mandelbrot(SettingsBase):

    _SETTINGS = {
        'bailout': 2.0,
        'max_iter': 128,
        'coloring': 'Default'
        }


@settings_class
class _Julia(SettingsBase):

    _SETTINGS = {
        'parameter_real': -0.12,
        'parameter_imag': 0.75,
        'bailout': 2.0,
        'max_iter': 128,
        'coloring': 'Default'
        }


def initialize():
    global canvas
    global mandelbrot
    global julia
    canvas = _Canvas()
    mandelbrot = _Mandelbrot()
    julia = _Julia()


if __name__ == '__main__':
    tk.Tk()
    s = _Canvas()
    print(s.get_size_x_var())
    print(s.size_x)
    s.size_x = 23
    print(s.size_x)
