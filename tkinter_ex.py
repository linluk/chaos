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

    # hidden options
    VALIDATE = 'validate'
    VALIDATECOMMAND = 'validatecommand'

    # additional options
    MAX_VALUE = 'maxvalue'
    MIN_VALUE = 'minvalue'

    def __init__(self, master, **options):
        self.max_value = None
        self.min_value = None
        if options:
            if self.MAX_VALUE in options:
                self.max_value = options[self.MAX_VALUE]
                del options[self.MAX_VALUE]
            if self.MIN_VALUE in options:
                self.min_value = options[self.MIN_VALUE]
                del options[self.MIN_VALUE]
        if not options:
            options = {}
        options[self.VALIDATE] = 'all'
        vcmd = (master.register(self._validate), '%P')
        options[self.VALIDATECOMMAND] = vcmd
        super().__init__(master, **options)

    def config(self, **options):
        if options:
            __error_if_keys_exist(self,
                                  [self.VALIDATE, self.VALIDATECOMMAND],
                                  options)
            if self.MAX_VALUE in options:
                self.max_value = options[self.MAX_VALUE]
                del options[self.MAX_VALUE]
            if self.MIN_VALUE in options:
                self.min_value = options[self.MIN_VALUE]
                del options[self.MIN_VALUE]
        return super().config(**options)

    def _validate(self, P):
        return self.validate(P)

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
        # override this method with your validation logic
        # return the value when it is valid
        # or none when it is invalid.
        return value



class IntEntry(ValidateEntry):

    def validate(self, value):
        try:
            print('int validate')
            if value:
                v = int(value)
                if not (self.check_min(v) and self.check_max(v)):
                    print('int validate (min/max)')
                    return None
            print('int validate value')
            return value
        except ValueError:
            print('int validate error')
            return None


class DoubleEntry(ValidateEntry):

    def validate(self, value):
        try:
            print('validate')
            if value:
                v = float(value)
                if not (self.check_min(v) and self.check_max(v)):
                    print('validate (min max) --> None')
                    return None
            print('validate (ok) --> value')
            return value
        except ValueError:
            return None

if __name__ == '__main__':

    class A:
        def __init__(self):
            self.x = 42

        def check(self, v):
            return v == self.x

    class B(A):
        def f(self, v):
            return self.check(v)

    b = B()
    b.f(23)
