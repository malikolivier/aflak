# aflak - Advanced Framework for Learning Astrophysical Knowledge

![Build status](https://api.travis-ci.org/malikolivier/aflak.svg?branch=master)

# Environment

Support Python3.

# Setup

    virtualenv -p python3 venv
    . ./venv/bin/activate
    pip install -r requirements.txt

# Open a FITS file

    python aflak.py my-fits-file.fits

The provided FITS file is required to have the following extensions:
 - 'FLUX': 3D data containing 2D luminosity component for each wavelength value
 - 'WAVE': 1D data containing value of each target wavelength

After some fiddling you should be able to get a window like below:

![Screen capture of the running GUI application](images/2017-11-13-screenshot.jpg?raw=true)


# To see a fits file header

    fold -w 80 foo.fits | less

# TODO

- Distribute through PyPI
- Include CI / code checking tools
- Show arbitrary sums over spectral data (currently only show one frame)
- Benchmark / Test with several fits files
- Include GUI way of loading new images
- Improve ROI drawing
- Histogram should use logarithm scale by default
