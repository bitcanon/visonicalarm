import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='visonicalarm',
    version='3.0.1',
    author='Mikael Schultz',
    author_email='bitcanon@pm.me',
    description='A simple library for the Visonic Alarm API written in Python 3.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bitcanon/visonicalarm',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'python-dateutil'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
