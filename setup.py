from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cs2gsi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Jan Mrzílek",
    description="CS2 Game State Integration Python reader",
    url="https://github.com/Lalucek/CS2GSI",
)
