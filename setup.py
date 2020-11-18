# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dclient",
    version="0.2.8",
    author="Jacob Bushman",
    author_email="jacob.matthew.bushman@endurance.com",
    description="Deployment Client API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stash.endurance.com/projects/DEVOPS/repos/deployment_client/browse",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "python-dotenv",
        "requests",
        "flask",
        "gunicorn",
	"connexion"
    ],
    python_requires=">=3.6"
)
