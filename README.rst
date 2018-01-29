===============================================================
aflak - Advanced Framework for Learning Astrophysical Knowledge
===============================================================

.. figure:: https://api.travis-ci.org/malikolivier/aflak.svg?branch=master
   :alt: Build status

Environment
===========

Support Python3.5+.

Install
=======

You can install `aflak` using any of the following methods.

Using pip
---------

This is the recommended way of installing aflak as a user. Please make sure
to install `aflak` for python 3.x. It will not work on python 2.x.

.. code :: bash

    pip install aflak


Depending on your python install, you should be able to run aflak form the
command line with any of these commands

.. code :: bash

    aflak            # This should work in most environment
    python -m aflak  # `python' should be the python 3.x interpreter!
    python3 -m aflak

Using .deb files
----------------

*Only `Debian Stretch` and `Ubuntu 17.10` are supported for now.*

Download the .deb file of the latest release from
https://github.com/malikolivier/aflak/releases

Install it with:

.. code :: bash

    sudo dpkg -i aflak-X.X.X-release.deb
    # If dependencies are missing, you should then run:
    sudo apt-get install -f

Remove it with:

.. code :: bash

    sudo apt-get remove aflak

From source locally
-------------------

.. code :: bash

    git clone https://github.com/malikolivier/aflak
    cd aflak
    virtualenv -p python3 venv
    . ./venv/bin/activate
    pip install -r requirements.txt
    ./run

Open a FITS file
================

::

    aflak my-fits-file.fits

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
-  Set a label on the histogram's Y-axis (flux [1E-17 erg/s/cm^2])
