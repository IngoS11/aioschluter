#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", encoding="utf-8") as file:
    install_requires = list(val.strip() for val in file.readlines())

with open("requirements-test.txt", encoding="utf-8") as file:
    tests_require = list(val.strip() for val in file.readlines())

setup(
    name="aioschluter",
    version="0.1.1",
    author="Ingo Sauerzapf ",
    description="Async Python wrapper for the Schluter-DITRA-E-WIFI thermostats API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/IngoS11/aioschluter",
    license="MIT License",
    packages=find_packages(exclude=["tests"]),
    package_data={"nettigo_air_monitor": ["py.typed"]},
    python_requires=">=3.9",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
    setup_requires=("pytest-runner"),
    tests_require=tests_require,
)
