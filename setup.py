import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visonicalarm",
    version="1.0.9",
    author="Mikael Schultz",
    author_email="mikael.schultz@outlook.com",
    description="A simple API library for the Visonic Alarm system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MikaelSchultz/visonicalarm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
