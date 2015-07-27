import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='simpledoc',
    version='0.1.0',
    description='Generate markdown from python docstrings.',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    url='https://github.com/michaelconnor00/simpledoc',
    license='MIT',
    author='Michael Connor',
    author_email='michaelconnor00@gmail.com',
    py_modules=find_packages(exclude=['tests*']),
    install_requires=[''],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',  # TODO make compatible
        'Programming Language :: Python :: 3.3',  # TODO make compatible
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)