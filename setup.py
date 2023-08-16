from setuptools import setup, find_packages

setup(
    name='build_MTV0.8',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here
    ],
    entry_points={
        'console_scripts': [
            'buildmt = buildMT.build_dataset:build'
        ],
    },
)
