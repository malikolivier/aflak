===============================================================
aflak - Advanced Framework for Learning Astrophysical Knowledge
===============================================================

.. figure:: https://api.travis-ci.org/malikolivier/aflak.svg?branch=master
   :alt: Build status

Environment
===========

Support Python3.

Setup
=====

::

    virtualenv -p python3 venv
    . ./venv/bin/activate
    pip install -r requirements.txt

Open a FITS file
================

::

    ./run my-fits-file.fits

The provided FITS file is required to have the following extensions:

- 'FLUX': 3D data containing 2D luminosity component for each wavelength value
- 'WAVE': 1D data containing value of each target wavelength

After some fiddling you should be able to get a window like below:

.. figure:: images/2017-11-13-screenshot.jpg?raw=true
   :alt: Screen capture of the running GUI application

Get sample FITS files
=====================

The Makefile contains a few recipes to get sample fits files.
Run make as below:

::

    make data/manga-7443-12703-LINCUBE.fits

To see a fits file header
=========================

::

    fold -w 80 foo.fits | less

TODO
====

-  Show arbitrary sums over spectral data (currently only show one frame)
-  Benchmark / Test with several fits files
-  Improve ROI drawing
-  Include GUI way of showing a fits header
-  Set a label on the histogram's Y-axis (flux [1E-17 erg/s/cm^2])
-  Add a compass showing North and East directions and a scale bar in the unit
   of arcsec on the image
