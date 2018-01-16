# Generate UI files

aflak/mainwindow_ui.py: aflak/mainwindow.ui
	pyuic5 $< > $@

aflak/AstroImageView_ui.py: aflak/AstroImageViewTemplate.ui
	pyuic5 $< > $@
