from setuptools import setup, find_packages

setup(
    name="cs2gsi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    author="Jan Mrzílek",
    description="CS2 Game State Integration Python reader",
    url="https://github.com/Lalucek/CS2GSI",
)
