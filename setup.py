from setuptools import setup

setup(
    name='banking',
    packages=['banking'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-marshmallow',
        'pytest',
        'coverage'
    ],
)
