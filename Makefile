# Generate UI files

.PHONY: pep8 release install upload clean

pep8:
	git ls-files | grep .py$ | grep -v _ui.py$ | xargs pycodestyle

UIs: aflak/mainwindow_ui.py \
     aflak/AstroImageView_ui.py \
     aflak/FitsHeaderWindow_ui.py \
     aflak/FitsHeaderForm_ui.py \
     aflak/AboutDialog_ui.py

# Generate UI source files
aflak/mainwindow_ui.py: aflak/mainwindow.ui
	pyuic5 $< > $@
	# QtDesigner does not support setText for separators. So we add it here
	sed -i 's/\(self.menuAnalyze.addSeparator()\)/\1.setText("ROI")/' $@

aflak/AstroImageView_ui.py: aflak/AstroImageViewTemplate.ui
	pyuic5 $< > $@

aflak/FitsHeaderWindow_ui.py: aflak/FitsHeaderWindow.ui
	pyuic5 $< > $@

aflak/FitsHeaderForm_ui.py: aflak/FitsHeaderForm.ui
	pyuic5 $< > $@

aflak/AboutDialog_ui.py: aflak/AboutDialog.ui
	pyuic5 $< > $@

cython: aflak/functions.pyx
	python setup.py build_ext --inplace

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
	./github-release.py

# Generate deb files for packaging on Debian-derived systems
all-deb: aflak-ubuntu17.10.deb aflak-ubuntu16.04.deb aflak-ubuntu14.04.deb \
         aflak-debian-stretch.deb aflak-debian-jessie.deb

aflak-ubuntu17.10.deb: release
	./make-deb.sh ubuntu17.10

aflak-ubuntu16.04.deb: release
	./make-deb.sh ubuntu16.04

aflak-ubuntu14.04.deb: release
	./make-deb.sh ubuntu14.04

aflak-debian-stretch.deb: release
	./make-deb.sh debian-stretch

aflak-debian-jessie.deb: release
	./make-deb.sh debian-jessie

clean:
	rm -rf *.deb
