#!/usr/bin/env python3
"""
Setup script for SecureVault
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="securevault",
    version="1.0.0",
    description="Local encrypted password manager with AES-256 encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Holy Grail Automation",
    author_email="",
    url="https://github.com/DonkRonk17/SecureVault",
    py_modules=["securevault"],
    install_requires=[
        "cryptography>=41.0.0",
    ],
    extras_require={
        "clipboard": ["pyperclip>=1.8.0"],
    },
    entry_points={
        "console_scripts": [
            "securevault=securevault:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="password manager security encryption aes-256 vault local cli",
)
