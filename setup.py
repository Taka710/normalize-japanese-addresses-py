import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="normalize-japanese-addresses",
    version="0.0.1",
    author="Takahiro Hama",
    author_email="taka710.py@gmail.com",
    maintainer="Takahiro Hama",
    maintainer_email="taka710.py@gmail.com",
    description="Ported version of @geolonia/normalize-japanese-addresses",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Taka710/normalize-japanese-addresses-py",
    project_urls={
        "Bug Tracker": "https://github.com/Taka710/normalize-japanese-addresses-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
