import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycargo", # Replace with your own username
    version="2.0.0",
    author="Taranjeet Singh",
    author_email="taranjeet.singh.3312@gmail.com",
    description="Pycargo is a utility to work with loading and exporting data from excel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/taranjeet.singh.3312/pycargo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['validators>=0.18.2,<2', 'openpyxl>=3.0.5,<4', 'pandas>=1.2.0,<2']
)