"""
This is setup file of the package.
"""
from setuptools import setup

setup(
    name="s23openalex",
    version="0.0.1",
    description="Openalex utilities",
    maintainer="Ruiying Chen",
    maintainer_email="ruiyingc@andrew.cmu.edu",
    license="MIT",
    packages=["s23openalex"],
    entry_points={"console_scripts": ["oa = s23openalex.main:main"]},
    long_description="""A set of openalex utilities""",
)
