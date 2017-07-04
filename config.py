import sys
import py2exe
from distutils.core import setup

sys.argv.append('py2exe')

setup(
    options={
        'py2exe':
        {
            'bundle_files': 1,
        }
    },
    console=[{'script': 'app4.py'}],
)
