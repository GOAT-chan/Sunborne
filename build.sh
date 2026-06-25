#!/bin/bash

uv run nuitka --mode=standalone \
              --clang \
              --assume-yes-for-downloads \
              --prefer-source-code \
              --output-filename=sunborne \
              --output-dir=publish \
              --remove-output \
              --deployment \
              --include-package=urllib3 \
              main.py