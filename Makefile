# Generate UI files

aflak/mainwindow_ui.py: aflak/mainwindow.ui
	pyuic5 $< > $@
