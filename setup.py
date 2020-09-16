import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="woetohice",
    version="0.0.1",
    author="Ryan De Villa",
    author_email="rdevilla@uwaterloo.ca",
    description="Scrapes transactions from TD statement PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryandv/woetohice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "woetohice=woetohice.__main__:main",
        ],
    },
)
