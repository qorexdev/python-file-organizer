"""Package setup for python-file-organizer."""

from setuptools import setup, find_packages

from organizer import __version__

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="python-file-organizer",
    version=__version__,
    description="CLI tool to auto-organize files by type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="qorexdev",
    url="https://github.com/qorexdev/python-file-organizer",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "organize=organizer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
