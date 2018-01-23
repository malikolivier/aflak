#!/usr/bin/env python3

import os
import re
import subprocess

import requests

from aflak.__init__ import __version__

changelog = ''
with open('CHANGELOG.rst') as f:
    version_re = re.compile('^v(\d+.\d+.\d+)$')
    equal_re = re.compile('^=+$')
    version_count = 0
    for line in f:
        if version_re.match(line):
            version_count += 1
            if version_count >= 2:
                break
            else:
                continue
        if equal_re.match(line):
            continue
        changelog += line
changelog = changelog.strip()

tag = 'v%s' % __version__
subprocess.run(['git', 'tag', tag], check=True)
subprocess.run(['git', 'push', 'origin', tag], check=True)
print('Posting release...')
subprocess.run(['make', 'all-deb'], check=True)
r = requests.post('https://api.github.com/repos/malikolivier/aflak/releases',
                  json={
                        'tag_name': tag,
                        'name': tag,
                        'body': changelog,
                        'draft': True
                  }, headers={
                        'Authorization': 'token %s' % os.getenv('GITHUB_TOKEN')
                  })
print(r.status_code)
json = r.json()
print(json)
release_id = json['id']

# ubuntu16.04 is not supported as it ships a too old version of
# python3-pyqtgraph (0.9.10-5). We want 0.10 or more.
SUPPORTED_PLATFORMS = ['ubuntu17.10', 'debian-stretch']

for asset in ['aflak-%s-%s.deb' % (__version__, platform)
              for platform in SUPPORTED_PLATFORMS]:
    uri = ('https://uploads.github.com/repos/malikolivier/aflak/'
           'releases/%s/assets?name=%s' % (release_id, asset))
    print('Posting release "%s"...' % asset)
    r = requests.post(uri, headers={
        'Content-Type': 'application/vnd.debian.binary-package',
        'Authorization': 'token %s' % os.getenv('GITHUB_TOKEN')
    }, data=open(asset, 'rb'))
    print(r.status_code)
    print(r.text)
