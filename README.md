collage
=======

Take a bunch of images and place them on a grid.

The script is quite configurable. All current config options are in the file
``settings.py``. To change them, make a file ``settings_local.py`` and
overwrite whichever settings you want.

Note: ``settings_local`` does not automatically inherit settings. If you want
to reuse settings from settings.py, do ``from settings import *`` at the top
of your settings file.


Acknowledgments
---------------

* Without the PIL (Python Image Library), this script would do... nothing.
* Thanks to Brenda Gallo for making the font "Happy Monkey", and thanks to
  Google Web Fonts for helping me find it.


License
-------

This software is licensed under a BSD License. Please read the file LICENSE
for more information.
