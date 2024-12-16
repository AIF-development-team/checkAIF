from setuptools import setup, find_packages

setup(
    name="checkAIF",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "gemmi",
        "datetime",
        "numpy",
        "pylint",
        "pre-commit",
    ],
)