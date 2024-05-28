from setuptools import find_packages
from setuptools import setup

setup(
    name='ras_urdf_common',
    version='0.0.0',
    packages=find_packages(
        include=('ras_urdf_common', 'ras_urdf_common.*')),
)
