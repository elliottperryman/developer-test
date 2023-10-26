from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="giskardSolution",  # Replace with your library name
    version="0.1.0",  # Update the version
    description="A simple Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/mylibrary",
    packages=['solution'], #find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],    
    # 'console_scripts': [ 'project=project.module:main'],
    entry_points={
        'console_scripts': [
            'give-me-the-odds=solution.main:main',
        ],
    },
)
