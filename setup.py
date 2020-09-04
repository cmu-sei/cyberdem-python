import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf8")
LICENSE = (HERE / "LICENSE.md").read_text(encoding="utf8")

setup(
    name="cyberdem",
    version="0.0.1",
    description="CyberDEM SISO standard python helper package",
    long_description=README,
    long_description_content_type="text/markdown",
    license=LICENSE,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["cyberdem"],
)
