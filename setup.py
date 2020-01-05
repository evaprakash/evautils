from distutils.core import setup, Extension
from setuptools import setup, Extension

config = {
    'include_package_data': True,
    'description': 'Helper scrips for benchmarking pipeline',
    'url': 'NA',
    'download_url': '',
    'version': '0.0.1',
    'packages': [],
    'setup_requires': [],
    'install_requires': [],
    'scripts': [],
    'name': 'evautils'
}

if __name__== '__main__':
    setup(**config)
