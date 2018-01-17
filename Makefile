# Generate UI files

.PHONY: pep8

pep8:
	git ls-files | grep .py$ | grep -v _ui.py$ | xargs pycodestyle

aflak/mainwindow_ui.py: aflak/mainwindow.ui
	pyuic5 $< > $@

aflak/AstroImageView_ui.py: aflak/AstroImageViewTemplate.ui
	pyuic5 $< > $@

data/manga-7443-12703-LINCUBE.fits:
	wget -O $@.gz \
	     https://data.sdss.org/sas/dr14/manga/spectro/redux/v2_1_2/7443/stack/manga-7443-12703-LINCUBE.fits.gz
	gzip -d $@.gz

data/manga-8081-1901-LINCUBE.fits:
	wget -O $@.gz \
	    https://data.sdss.org/sas/dr14/manga/spectro/redux/v2_1_2/8081/stack/manga-8081-1901-LINCUBE.fits.gz
	gzip -d $@.gz

data/manga-8082-12704-LINCUBE.fits:
	wget -O $@.gz \
	    https://data.sdss.org/sas/dr14/manga/spectro/redux/v2_1_2/8082/stack/manga-8082-12704-LINCUBE.fits.gz
	gzip -d $@.gz
