#!/usr/bin/env bash

rm -rf build
rm -rf dist

python setup.py bdist_wheel
python -m twine upload dist/*