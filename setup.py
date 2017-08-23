from setuptools import setup

setup(
    name='Web Utils',
    version='1.0',
    py_modules=['webutils'],
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