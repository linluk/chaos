CHAOS
=====

chaos.py is going to be a fractal generator for mandelbrot
and julia sets.


INSTALL
-------

1. Create a Virtual Environment with 'python3 -m venv venv' in the projects
   root directory

2. Activate the Virtual Environment with '. venv/bin/activate'

3. Install the Requirements with 'pip install -r requirements.txt'

4. Have fun with fractals!


PROBLEMS:
---------

* If you have troubles installing Pillow (from the requirements.txt) chances are
  that there are missing dependencies.
  This worked for me
  'apt install libjpeg9 zlibc libtiff5 libfreetype6 liblcms2-2 libwebp5 \
  openjpeg-tools libjpeg9-dev zlib1g zlib1g-dev libtiff5-dev libfreetype6-dev \
  liblcms2-dev openjpeg-tools libjpeg-dev python3-dev'

* If you run in an error like this:
  'ImportError: cannot import name '_imagingtk''
  you have to rebuild Pillow with tk/tcl support.

  1. find out wich version of tk/tcl your python version is using:
     run: 'python -m tkinter'. My version was 8.6

  2. Install development libs: 'apt install tk8.6-dev tcl8.6-dev'

  3. Rebuild Pillow: 'pip install --force-reinstall --ignore-installed Pillow'

  4. Sources:
     4.1. https://github.com/python-pillow/Pillow/issues/322