v0.0.7
======

New:

- Add icon to debian release


v0.0.6
======

New:

- Make .deb files for easy distribution

Fix:

- Force use of PyQt5, even if PyQt4 happen to be installed (28cb7a0)
- Increase size of ROI handles, making them easier to be grabbed (e533168)


v0.0.5
======

New:

- Add 3 types of ROI: polygonal, ecliptic and semi-automatic. In semi-automatic
  mode, the use is free to choose and point and a threshold. All the points
  above the threshold around the selected point will be inside the ROI.
- Add a "Recent Files" menu. No need to look far away for your FITS files.

Change:

- Delete ROI button and move ROI management inside menu.

Fix:

- Output of --version under some some circumstances (fa7e211)
- Name of main window is set to 'aflak' (6677775)


v0.0.4
======

New:

- FITS menu from which FITS header can be seen
- Version flag to CLI
- `About' dialog box in Help menu


v0.0.3
======

Fix: Run aflak as module (with `python -m aflak`)

New:

- Include some unit tests
- Include units in waveform axes, read from loaded FITS files


v0.0.2
======

Fix: Use logarithmic scale on brightness histograms


v0.0.1
======

Very first version released on PyPI. Can only open FITS files and visualize
FLUX and WAVE data.
