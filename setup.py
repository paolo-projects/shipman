from setuptools import setup, find_packages

setup(
    name='Shipman',
    version='1.0.4',
    url='https://github.com/paolo-projects/shipman',
    author='Paolo',
    license='GPLv3',
    install_requires=[
        'requests',
        'argcomplete'
    ],
    packages=find_packages(),
    scripts=['bin/shipman']
)