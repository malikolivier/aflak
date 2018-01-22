#!/usr/bin/env bash

# Script to generate .deb installer file

set -e
set -u

TARGET_DISTRO=$1

case "$TARGET_DISTRO" in
    ubuntu17.10)
        PY_VERSION=3.6
        ;;
    ubuntu16.04)
        PY_VERSION=3.5
        ;;
    ubuntu14.04)
        PY_VERSION=3.4
        ;;
    debian-stretch)
        PY_VERSION=3.5
        ;;
    debian-jessie)
        PY_VERSION=3.4
        ;;
    *)
        echo "Usage: $0 distro_name"
        echo "Unknown distro: $TARGET_DISTRO"
        exit 1
esac
NEXT_PY_VERSION=$(echo "$PY_VERSION" | awk -F. '{print $1"."($2+1)}')

AFLAK_VERSION=$(grep -o "[0-9]\.[0-9]\.[0-9]" aflak/__init__.py)

WORK=dist-deb
BINDIR="$WORK"/data/usr/bin
LIBDIR="$WORK"/data/usr/lib
PYTHONPKGDIR="$LIBDIR"/python"$PY_VERSION"/dist-packages

# Clean work dir
rm -rf "$WORK"

# Make "data.tar.gz"
mkdir -p "$BINDIR"
cp run "$BINDIR"/aflak

mkdir -p "$PYTHONPKGDIR"
tar -xf dist/aflak-"$AFLAK_VERSION".tar.gz -C "$WORK"
mv "$WORK"/aflak-"$AFLAK_VERSION"/{aflak,aflak.egg-info} "$PYTHONPKGDIR"

cd "$WORK"/data
tar -zcf ../data.tar.gz .
cd - > /dev/null

# Make "control.tar.gz"

CONTROLDIR="$WORK"/control

mkdir -p "$CONTROLDIR"
INSTALLED_SIZE=$(zcat "$WORK"/data.tar.gz | wc -c | awk '{print int($1/1024)}')
cat > "$CONTROLDIR"/control <<EOF
Package: aflak
Version: $AFLAK_VERSION-1
Architecture: all
Maintainer: Malik Oliver Boussejra <malik@boussejra.com>
Original-Maintainer: Malik Oliver Boussejra <malik@boussejra.com>
Installed-Size: $INSTALLED_SIZE
Depends: python3-astropy, python3-pyqt5, python3-pyqtgraph, python:any (<< $NEXT_PY_VERSION), python3:any (>= $PY_VERSION.0-1~)
Recommends:
Suggests:
Section: python
Priority: optional
Homepage: https://aflak.jp/
Description: aflak - Advanced Framework for Learning Astrophysical Knowledge
 Spectral analysis on FITS files
EOF

cd "$CONTROLDIR"
tar -zcf ../control.tar.gz *
cd - > /dev/null

# Make "debian-binary"
echo 2.0 > "$WORK"/debian-binary

# Make package
ar r aflak-"$AFLAK_VERSION"-"$TARGET_DISTRO".deb "$WORK"/{debian-binary,control.tar.gz,data.tar.gz}
