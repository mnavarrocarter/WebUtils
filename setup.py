from setuptools import setup, find_packages

setup(
    name='Web Utils',
    version='1.1',
    url='https://github.com/mnavarrocarter/WebUtils',
    description='A python cli tool for web developers in Ubuntu derivatives.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    # This creates an auto-executable called webutils that points to
    # webutils cli() method.
    entry_points='''
        [console_scripts]
        webutils=src.webutils:cli
    ''',
)