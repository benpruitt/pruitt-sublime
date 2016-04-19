
import shutil
import os

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))
TARGET_DIR = '~/Library/Application Support/Sublime Text 3/Packages/User/'

td = os.path.expanduser(TARGET_DIR)

files_to_copy = [
    'seq.py',
    'spancomment.py',
    'tm.py',
    'util.py',
    'Context.sublime-menu'
]

assert os.path.isdir(td)

for fn in files_to_copy:
    shutil.copy(
        os.path.join(LOCAL_DIR, fn),
        os.path.join(td, fn)
    )
