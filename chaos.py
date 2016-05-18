#!/usr/bin/env python

import tkinter as tk
import time

import complex_plane as cp

class Mandelbrot:
  def __init__(self):
    self.root = tk.Tk()
    self.complex_plane = None # cp.ComplexPlane()
    self.img_container = tk.Label(self.root)#,
                                  #image=self.complex_plane.get_tk_image())
    self.img_container.bind('<Motion>', self.mouse_move)
    self.img_container.pack()
    self.btn = tk.Button(self.root, text='render', command=self.render)
    self.btn.pack()
    self.coords = tk.StringVar()
    self.coords.set('###')
    self.lbl = tk.Label(self.root, textvariable=self.coords)
    self.lbl.pack()
#        self.render()
    self.root.mainloop()

  def mouse_move(self, event):
    if self.complex_plane:
      x, y = event.x, event.y
      z = self.complex_plane.p2c((x, y))
      self.coords.set('({}, {})  {}'.format(z, x, y))
    else:
      self.coords.set('###')

  def render(self):
    t0 = time.clock()
    imax = 256
    self.complex_plane = cp.ComplexPlane((400, 300), (3, 3))
    for c, p in self.complex_plane:
      z = 0
      icnt = 0
      while abs(z) < 2.0 and icnt < imax:
        z = z * z + c
        icnt += 1
        if icnt >= imax:
          self.complex_plane.set_pixel(p, '#0808ff')
        else:
          self.complex_plane.set_pixel(p, '#ff0000')
    t1 = time.clock()
    self.img_container.configure(image = self.complex_plane.get_tk_image())
    print('rendered mandelbrot in {:.3f} seconds'.format(t1 -t0))

if __name__ == '__main__':
  m = Mandelbrot()
