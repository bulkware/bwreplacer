#!/bin/bash

# Build a multi-resolution Windows icon so it stays sharp in shell and menu views.
# ImageMagick starts with the source image and appends each requested size.
convert icon.png \
    \( -clone 0 -resize 16x16 \) \
    \( -clone 0 -resize 32x32 \) \
    \( -clone 0 -resize 48x48 \) \
    \( -clone 0 -resize 64x64 \) \
    \( -clone 0 -resize 128x128 \) \
    \( -clone 0 -resize 256x256 \) \
    -alpha background -delete 0 icon.ico
