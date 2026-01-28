"""Setup script for ScreenshotScanner package."""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ScreenshotScanner",
    version="0.1.0",
    author="AzwadFawadHasan",
    author_email="azwadfawadhasan@gmail.com",
    description="A heuristic-based tool to detect whether an image is a screenshot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AzwadFawadHasan/ScreenshotScanner",
    project_urls={
        "Bug Tracker": "https://github.com/AzwadFawadHasan/ScreenshotScanner/issues",
        "Documentation": "https://github.com/AzwadFawadHasan/ScreenshotScanner#readme",
        "Source Code": "https://github.com/AzwadFawadHasan/ScreenshotScanner",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="screenshot detection image-processing document-verification kyc",
    include_package_data=True,
)
