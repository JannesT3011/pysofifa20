from setuptools import setup
import setuptools

with open("README.md", "r") as ld:
    long_description = ld.read()

setup(
    name="pysofifa20",
    version="0.1",
    author="Bmbus",
    description="Get data from sofifa20",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bmbus/pysofifa20/blob/master/setup.py",
    packages=setuptools.find_packages(),
    install_requires=["bs4"],
    python_requires=">=3.7"
)