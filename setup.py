import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visonicalarm",
    version="1.0.0",
    author="Mikael Schultz",
    author_email="mikael@dofiloop.com",
    description="A simple library for the Visonic Alarm API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MikaelSchultz/visonicalarm",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
