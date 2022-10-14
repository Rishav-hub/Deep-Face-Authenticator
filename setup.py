from setuptools import find_packages, setup

# Declaring variables for setup functions
PROJECT_NAME = "Face Authenticator"
VERSION = "0.0.1"
AUTHOR = "Rishav Dash"
DESRCIPTION = "This is a Face Authenticator Project"


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESRCIPTION,
    packages=find_packages(),
)
