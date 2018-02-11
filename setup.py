import io
import re
from os.path import dirname
from os.path import join

from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def get_version():
    f = open('aflak/__init__.py')
    version_re = re.compile("^__version__ = '(\d+\.\d+\.\d+)'$")
    for line in f:
        match = version_re.match(line)
        if match:
            return match.group(1)
    raise "Version not found"


setup(name='aflak',
      version=get_version(),
      python_requires='>=3',
      description='Advanced Framework for Learning Astrophysical Knowledge',
      long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges',
                   re.M | re.S).sub('',  read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
      ),
      author='Malik Olivier Boussejra',
      author_email='malik@boussejra.com',
      url='https://github.com/malikolivier/aflak',
      license='GPLv3',
      packages=['aflak'],
      entry_points={
          'console_scripts': [
              'aflak = aflak.aflak:main',
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
