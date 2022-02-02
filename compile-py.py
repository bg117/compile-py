import sys
from zipfile import ZipFile
import os


def list_to_str(lst: list) -> str:
    return ' '.join(lst)

# concat multiple scripts (for *nix OSes only)


if len(sys.argv) == 1:
    print('Usage: python3 compile-py.py <scripts_dir> <output_file>')
    sys.exit(0)

print('Compile Python scripts into a UNIX executable')

# path is in argv[1]
scripts_dir = sys.argv[1]
out = sys.argv[2]

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

# convert the files to a .zip file using ZipFile
with ZipFile(out, 'w') as zip_file:
    for file in files:
        print('Adding {} to {}'.format(file, out))
        zip_file.write(os.path.join(file))

# prepend #!/usr/bin/env python3 to the zip file
with open(out, 'r+b') as zip_file:
    zip_file.seek(0)
    zip_file.write(b'#!/usr/bin/env python3\n')
    zip_file.seek(0)

# make the zip file executable
os.chmod(out, 0o755)

print('Done! Output file: ' + out)
