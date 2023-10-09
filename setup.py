#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


env_marker_cpython = (
    "sys_platform != 'win32'"
    " and (sys_platform != 'cygwin'"
    " and platform_python_implementation != 'PyPy')"
)

env_marker_win = "sys_platform == 'win32'"
env_marker_below_38 = "python_version < '3.8'"

minimal_requirements = [
    "click~=8.1.3",
    "PyYAML~=6.0",
    "Jinja2~=3.1.2",
    "setuptools~=65.5.1",
    "six~=1.16.0",
    "rich~=13.6.0",
    "Pygments~=2.16.1",
]

test_requirements = {
    "altgraph==0.17.3",
    "argcomplete==2.0.0",
    "attrs==22.1.0",
    "cachetools==5.3.1",
    "chardet==5.2.0",
    "click==8.1.3",
    "colorama==0.4.6",
    "colorlog==6.7.0",
    "distlib==0.3.7",
    "exceptiongroup==1.0.4",
    "filelock==3.12.4",
    "future==0.18.3",
    "iniconfig==1.1.1",
    "Jinja2==3.1.2",
    "markdown-it-py==3.0.0",
    "MarkupSafe==2.1.1",
    "mdurl==0.1.2",
    "packaging==23.2",
    "pefile==2022.5.30",
    "Pillow==10.0.1",
    "platformdirs==3.11.0",
    "pluggy==1.3.0",
    "Pygments==2.16.1",
    "pyinstaller==5.7.0",
    "pyinstaller-hooks-contrib==2022.15",
    "pyproject-api==1.6.1",
    "pytest==7.2.0",
    "python-magic-bin==0.4.14",
    "pywin32-ctypes==0.2.0",
    "PyYAML==6.0",
    "rich==13.6.0",
    "six==1.16.0",
    "tomli==2.0.1",
    "tox==4.11.3",
    "typing_extensions==4.8.0",
    "virtualenv==20.24.5",
}


setup(
    name="Easy-Template",
    version="0.0.2",
    url="https://github.com/camratchford/easy-template",
    license="CC0 1.0 Universal",
    description="Quick and Dirty jinja templating from CLI and YAML",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Cam Ratchford",
    author_email="cameron@ratchfordconsulting.com",
    packages=get_packages('ez_temp'),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=minimal_requirements,
    extras_require={"test": test_requirements},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Administrators",
        "License :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': {
            'ezt = ez_temp.cli:run',
        }
    },
    project_urls={
        "Funding": "https://github.com/sponsors/camratchford",
        "Source": "https://github.com/camratchford/easy-template",
        "Changelog": "https://github.com/camratchford/easy-template/blob/master/CHANGELOG.md",
    },
)