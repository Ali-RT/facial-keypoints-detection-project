#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = []

setup(
    author="ART",
    author_email="alirahimtaleqani@gmail.com",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="This porject trains a convolutional neural network (CNN) specifically designed for facial keypoint detection",
    entry_points={
        "console_scripts": [
            "facial_keypoints_detection=facial_keypoints_detection.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="facial_keypoints_detection",
    name="facial_keypoints_detection",
    packages=find_packages(include=["facial_keypoints_detection", "facial_keypoints_detection.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Ali-RT/facial_keypoints_detection",
    version="0.1.1",
    zip_safe=False,
)
