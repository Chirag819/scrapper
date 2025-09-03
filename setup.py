#!/usr/bin/env python3
"""
Setup script for SaaS Review Scraper
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="scrapper",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@domain.com",
    description="A powerful Python script to scrape product reviews from multiple SaaS review platforms",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Chirag819/scrapper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "saas-scraper=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="web-scraping, reviews, saas, capterra, trustpilot, g2, selenium, beautifulsoup",
    project_urls={
        "Bug Reports": "https://github.com/Chirag819/scrapper/issues",
        "Source": "https://github.com/Chirag819/scrapper",
        "Documentation": "https://github.com/Chirag819/scrapper#readme",
    },
)