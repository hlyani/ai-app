from setuptools import setup, find_packages

PACKAGE = "app"
VERSION = "0.0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="app",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "app = app.main:main",
        ],
    }
)
