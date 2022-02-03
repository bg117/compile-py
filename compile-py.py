#!/usr/bin/env python3

from re import T
import sys
from zipfile import ZipFile
import os
import zipfile


def list_to_str(lst: list) -> str:
    return ' '.join(lst)


if len(sys.argv) == 1:
    print(
        'Usage: python3 compile-py.py <scripts_dir> <output_file> [--no-ext]')
    sys.exit(0)

print('Compile multiple Python scripts into a single .py file')

# path is in argv[1]
scripts_dir = sys.argv[1]
out = sys.argv[2]

# if out doesn't end with .py, add it
if not out.endswith('.py'):
    out += '.py'

# check if "--no-ext" is in argv
if '--no-ext' in sys.argv:
    out = out[:-3]

# check if scripts_dir exists
if not os.path.isdir(scripts_dir):
    print('{} does not exist'.format(scripts_dir))
    sys.exit(1)

# recursively get all the .py files in scripts_dir
files = []
for root, dirs, tmp_files in os.walk(scripts_dir):
    for file in tmp_files:
        if file.endswith('.py'):
            files.append(os.path.join(root, file))

print('Found {} files in {}.\n\t{}'.format(
    len(files), scripts_dir, list_to_str(files)))

# check if __main__.py exists
if not os.path.isfile(os.path.join(scripts_dir, '__main__.py')):
    print('__main__.py does not exist in {}'.format(scripts_dir))
    sys.exit(1)

# convert files into .zip file with relative paths
with ZipFile(out, 'w') as zip:
    for file in files:
        zip.write(file, os.path.relpath(file, scripts_dir))

print('Done! You can run the output file with:\n\tpython3 {}'.format(out))
