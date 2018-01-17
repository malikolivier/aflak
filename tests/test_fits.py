from aflak.fits import FITS

def test_flux_unit():
    f = FITS('data/manga-7443-12703-LINCUBE.fits')
    assert f.flux_unit() == '1E-17 erg/s/cm^2/Ang/spaxel'

def test_summed_flux_unit():
    f = FITS('data/manga-7443-12703-LINCUBE.fits')
    assert f.summed_flux_unit() == '1E-17 erg/s/cm^2/spaxel'
