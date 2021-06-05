import setuptools
from distutils.core import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="normalize-japanese-addresses",
    version="0.0.1.3",
    author="Takahiro Hama",
    author_email="taka710.py@gmail.com",
    maintainer="Takahiro Hama",
    maintainer_email="taka710.py@gmail.com",
    description="Ported version of @geolonia/normalize-japanese-addresses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    url="https://github.com/Taka710/normalize-japanese-addresses-py",
    project_urls={
        "Bug Tracker": "https://github.com/Taka710/normalize-japanese-addresses-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "requests",
        "requests_cache",
        "kanjize"
    ],
    python_requires=">=3.8",
)
