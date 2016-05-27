#!/usr/bin/env python

from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk

class ComplexPlane:

  class ComplexPlaneIterator:

    def __init__(self, pixel_size, p2c):
      """ creates the iterator for complex planes """
      super().__init__()
      self.p2c = p2c
      self.w, self.h = pixel_size
      self.p = 0, -1 # we inc first

    def __iter__(self):
      """ an iterator has to return itself as an iterator """
      return self

    def __next__(self):
      """ returns the next pair of pixel- and complex coord """
      x, y = self.p
      y += 1
      if y >= self.h:
        y = 0
        x += 1
        if x >= self.w:
          raise StopIteration()
      self.p = (x, y)
      return self.p2c(self.p), self.p

  def __init__(self,
               width, height, # in pixels
               start, end):   # complex coordinates
    """ creates a complex plane """
    super().__init__()
    self.img = Image.new("RGB", (width, height))
    self.draw = ImageDraw.Draw(self.img)
    self.start = complex(start)
    self.end = complex(end)
    self.delta = complex((self.end.real - self.start.real) / width,
                         (self.end.imag - self.start.imag) / height)

  def __iter__(self):
    return ComplexPlane.ComplexPlaneIterator(
      self.img.size,
      self.p2c)

  def c2p(self, z):
    """ returns the pixel coord for complex z """
    z = (z - self.start) * self.delta
    return (int(z.real + 0.5), int(z.imag + 0.5))

  def p2c(self, p):
    """ returns the complex coord for pixel p """
    return complex(p[0] * self.delta.real, p[1] * self.delta.imag) + self.start

  def set_pixel(self, p, color):
    """ sets the pixel p to color """
    self.draw.point(p, color)

#  def get_pixel(self, p):
#    """ returns the color of pixel p """
#    return self.image.get(p)

  def set_complex(self, z, color):
    """ sets the corresponding pixel of complex z to color """
    self.set_pixel(self.c2p(z), color)

#  def get_complex(self, z):
#    """ returns the color of the pixel coresponding to complex z """
#    return self.get_pixel(self.c2p(z))

  def get_pil_image(self):
    return self.img

  def get_tk_image(self):
    """ returns an tkinter.PhotoImage instance for
    """
    tki = ImageTk.PhotoImage(self.img)
     # we need to keep a reference, otherwise gc would kick in by mistake
    self.__work_around = tki
    return tki
