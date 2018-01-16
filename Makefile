# Generate UI files

.PHONY: pep8

pep8:
	git ls-files | grep .py$ | grep -v _ui.py$ | xargs pycodestyle

aflak/mainwindow_ui.py: aflak/mainwindow.ui
	pyuic5 $< > $@

aflak/AstroImageView_ui.py: aflak/AstroImageViewTemplate.ui
	pyuic5 $< > $@
