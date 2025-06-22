from setuptools import setup, find_packages

setup(
    name='adiftools',
    version='0.1.7',
    description='ADIF file utilities',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='JS2IIU',
    author_email='info@js2iiu.com',
    maintainer='JS2IIU',
    maintainer_email='info@js2iiu.com',
    url='https://github.com/JS2IIU-MH/adiftools-dev',
    download_url='https://github.com/JS2IIU-MH/adiftools-dev',
    packages=find_packages(
        include=['adiftools', 'adiftools.*'],
        exclude=['test/']),
    # package_dir = {"": "adiftools"},
    install_requires=open('requirements.txt').readlines(),
    keywords=['adif'],
    license='MIT',
)
