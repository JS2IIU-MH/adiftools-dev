from setuptools import setup, find_packages

setup(
    name='adiftools',
    version='0.0.1',
    description='ADIF file parser',
    author='JS2IIU',
    author_email='info@js2iiu.com',
    url='https://github.com/JS2IIU-MH/adiftools-dev',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
)