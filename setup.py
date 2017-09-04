from setuptools import setup, find_packages

setup(
    name='Rush',
    version='0.3',
    url='https://github.com/mnavarrocarter/rush',
    description='A cli tool written in pyhton for rushing web developers.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    # This creates an auto-executable called rush that points to
    # rush cli() method.
    entry_points='''
        [console_scripts]
        rush=src.rush:cli
    ''',
)