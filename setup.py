from setuptools import find_packages, setup

setup(
    name="jupyter-notebook-cleanup",
    version="1.2.0",
    description="Automagically remove notebook outputs for better security",
    author="Hiroyuki Tanaka",
    author_email="aflc0x@gmail.com",
    packages=find_packages(),
    python_requires=">=3",
    install_requires=[],
    entry_points={"console_scripts": ["jupyter-notebook-cleanup=jupyter_notebook_cleanup.cli:main"]},
)
