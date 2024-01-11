from setuptools import setup, find_packages

setup(
    name="shigg",
    version="0.2.2",
    packages=find_packages(),
    include_package_data=True,
    description="A bad Gui Library for games.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wegfawefgawefg/shigg",
    author="Gibson Martin",
    author_email="668es218pur@gmail.com",
    license="GPLv3",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
