from os.path import abspath, dirname, join
from setuptools import setup, find_packages

INIT_FILE = join(dirname(abspath(__file__)), 'justified_demo', '__init__.py')

def get_version():
    with open(INIT_FILE) as fd:
        for line in fd:
            if line.startswith('__version__'):
                version = line.split()[-1].strip('\'')
                return version
        raise AttributeError('Package does not have a __version__')

setup(
    name='justified_demo',
    description='Text-justification demo',
    #long_description=open('README.rst').read(),
    url="http://github.com/benjamin9999/justified_demo/",
    version=get_version(),
    author='Benjamin Yates',
    author_email='benjamin@rqdq.com',
    packages=['justified_demo'],
    install_requires=['urwid_pydux==0.2.0', 'justified==0.1.0'],
    license='MIT',
)
