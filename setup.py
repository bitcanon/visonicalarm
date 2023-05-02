import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvisonicalarm",
    version="0.1.0b0",
    author="Mark Parker",
    author_email="msparker@sky.com",
    description="A simple library for the Visonic Alarm API written in Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msp1974/pyvisonicalarm",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
