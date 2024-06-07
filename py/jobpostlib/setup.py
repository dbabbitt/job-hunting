
from setuptools import setup, find_packages

setup(
    name='notebook_utils',
    version='0.1.0',
    packages=find_packages(),
    description='This package implements the core of the utility functions needed to run Jupyter notebooks',
    author='Dave Babbitt',
    author_email='dave.babbitt@gmail.com',
    install_requires=['IPython', 'bs4', 'cycler', 'humanize', 'importlib', 'matplotlib', 'numpy', 'pandas', 'pysan', 'roman', 'scipy', 'seaborn', 'statistics', 'tqdm', 'typing', 'webcolors', 'wikipedia'],
)
