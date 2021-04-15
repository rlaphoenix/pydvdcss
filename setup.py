from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="pydvdcss",
    version="1.1.0",
    author="PHOENiX",
    author_email="rlaphoenix@pm.me",
    description="Python wrapper for VideoLAN's libdvdcss.",
    license="GPLv3",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rlaPHOENiX/pydvdcss",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Conversion"
    ],
    python_requires=">=3.6",
)
