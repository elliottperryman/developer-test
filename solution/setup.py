from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="giskardSolution",  
    version="1.0",  # Update the version
    description="(attempted) Solution of Giskard Developer Task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Elliott Perryman",
    author_email="elliott.perryman@hey.com",
    url="https://github.com/elliottperryman/developer-test",
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
