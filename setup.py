from setuptools import setup


setup(name='aflak',
      version='0.0.1',
      description='Advanced Framework for Learning Astrophysical Knowledge',
      author='Malik Olivier Boussejra',
      author_email='malik@boussejra.com',
      url='https://github.com/malikolivier/aflak',
      license='GPLv3',
      packages=['aflak'],
      entry_points={
          'console_scripts': [
              'aflak = aflak.__main__:_main',
          ]
      },
      install_requires=[
          'astropy',
          'pyqtgraph',
          'PyQt5',
      ],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Scientific/Engineering :: Visualization'
      ])
