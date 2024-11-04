from setuptools import setup, find_packages
from kettled.constants.env import VERSION

setup(
    name="kettled",
    version=VERSION,
    description="A lightweight and secure python scheduler",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="solarvenom",
    author_email="contact@solarvenom.com",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
)