from setuptools import setup, find_packages

requires = [
    "loguru>=0.7.3",
    "PyYAML>=5.1",
    "questionary>=2.0.0",
    "pydantic>=2.0.0",
]

setup(
    name='tuack',
    version='0.1.6',
    packages=find_packages(),
    description='Tools for migrating tuack contest projects to tuack-ng format.',
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'tuack=tuack.cli:main'
        ]
    },
)
