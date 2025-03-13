import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="contentgenerator",
    version="0.0.1",
    author="Chemali Technologies",
    author_email="sami@chemali.de",
    description="A Content Generator that utilizes an LLM and internet scraping to dynamically generate well-structured documents of varying lengths, rich in information and traditionally partitioned.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chemalii/ContentGenerator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)