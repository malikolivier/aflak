import argparse
import fitsio

parser = argparse.ArgumentParser(description='Provide FITS file as input')
parser.add_argument('fits', metavar='fits-file', help='FITS file to open')

args = parser.parse_args()

fits = fitsio.FITS(args.fits)
print(fits)
