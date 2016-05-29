#!/usr/bin/env python
"""
Filename: tkinter_ex.py
Author: Lukas Singer <lukas42singer (at) gmail (dot) com>
Created: 2016/05/29
Copyright: 2016, Lukas Singer
License: WTFPL (see COPYING or <http://www.wtfpl.net/>)
Description: Some additional or slightliy changed tkinter widgets.
"""


import tkinter as tk


def __error_if_keys_exist(inst, keys, dct):
    for key in keys:
        if key in dct:
            raise AttributeError(
                '{key} is not accessible in {inst}'.format(
                    key=key, inst=type(inst).__name__))


class Menu(tk.Menu):

    def __init__(self, master=None, **options):
        if not options:
            options = {}
        options['tearoff'] = 0
        super().__init__(master, **options)


class ValidateEntry(tk.Entry):

    # additional options
    MAX_VALUE = 'maxvalue'
    MIN_VALUE = 'minvalue'
    TEXT_VARIABLE = 'textvariable'

    def __init__(self, master=None, **options):
        self.max_value = None
        self.min_value = None
        self.variable = None
        self.variable_observer = None
        self.old_value = ''
        self.validate_variable = tk.StringVar()
        self.validate_variable.trace('w', self._validate)
        self.shortcut_validation = False
        self.ignore_variable_callback = False
        if options:
            if self.MAX_VALUE in options:
                self.max_value = options[self.MAX_VALUE]
                del options[self.MAX_VALUE]
            if self.MIN_VALUE in options:
                self.min_value = options[self.MIN_VALUE]
                del options[self.MIN_VALUE]
            if self.TEXT_VARIABLE in options:
                textvariable = options[self.TEXT_VARIABLE]
                del options[self.TEXT_VARIABLE]
        if not options:
            options = {}
        options[self.TEXT_VARIABLE] = self.validate_variable
        super().__init__(master, **options)
        self._set_textvariable(textvariable)

    def config(self, **options):
        if options:
            if self.MAX_VALUE in options:
                self.max_value = options[self.MAX_VALUE]
                del options[self.MAX_VALUE]
            if self.MIN_VALUE in options:
                self.min_value = options[self.MIN_VALUE]
                del options[self.MIN_VALUE]
            if self.TEXT_VARIABLE in options:
                self._set_textvariable(options[self.TEXT_VARIABLE])
                del options[self.TEXT_VARIABLE]
        return super().config(**options)

    def _set_textvariable(self, textvariable):
        if self.variable and self.variable_observer:
            self.variable.trace_vdelete('w', self.variable_observer)
        self.variable = textvariable
        self.variable_observer = self.variable.trace('w',
                                                     self._variable_changed)
        self._variable_changed()

    def _variable_set(self, value):
        try:
            self.ignore_variable_callback = True
            self.variable.set(value)
        finally:
            self.ignore_variable_callback = False

    def _force_value(self, value):
        try:
            self.shortcut_validation = True
            self.validate_variable.set(value)
        finally:
            self.shortcut_validation = False

    def _variable_changed(self, *dummy):
        if not self.ignore_variable_callback:
            value = self.variable.get()
            if self.validate(value):
                self._force_value(value)
            else:
                self.variable.set(self.old_value)

    def _validate(self, *dummy):
        value = self.validate_variable.get()
        if self.shortcut_validation:
            self.old_value = value
            self._variable_set(value)
        elif self.validate(value):
            self.old_value = value
            self._variable_set(value)
        else:
            self._force_value(self.old_value)

    def check_min(self, value):
        if self.min_value:
            return value >= self.min_value
        else:
            return True

    def check_max(self, value):
        if self.max_value:
            return value <= self.max_value
        else:
            return True

    def validate(self, value):
        # override this method with your validation logic.
        # return True if it is valid or False when invalid.
        return True


class IntEntry(ValidateEntry):

    def validate(self, value):
        try:
            if value:
                v = int(value)
                if not (self.check_min(v) and self.check_max(v)):
                    return False
                return True
            else:
                return False
        except ValueError:
            return False


class DoubleEntry(ValidateEntry):

    def validate(self, value):
        try:
            if value:
                v = float(value)
                if not (self.check_min(v) and self.check_max(v)):
                    return False
                return True
            else:
                return False
        except ValueError:
            return False
