# Generate UI files

.PHONY: pep8 release install upload

pep8:
	git ls-files | grep .py$ | grep -v _ui.py$ | xargs pycodestyle

UIs: aflak/mainwindow_ui.py \
     aflak/AstroImageView_ui.py \
     aflak/FitsHeaderWindow_ui.py \
     aflak/FitsHeaderForm_ui.py

# Generate UI source files
aflak/mainwindow_ui.py: aflak/mainwindow.ui
	pyuic5 $< > $@

aflak/AstroImageView_ui.py: aflak/AstroImageViewTemplate.ui
	pyuic5 $< > $@

aflak/FitsHeaderWindow_ui.py: aflak/FitsHeaderWindow.ui
	pyuic5 $< > $@

aflak/FitsHeaderForm_ui.py: aflak/FitsHeaderForm.ui
	pyuic5 $< > $@

# Download test samples from the MaNGA project
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

# Make a release build
release:
	rm -rf dist build */*.egg-info *.egg-info
	python setup.py sdist

# Install release locally
install: release
	python setup.py install

# Push release to PyPI
upload: release
	twine upload dist/*
