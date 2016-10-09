from setuptools import setup

author = 'Helium'
author_email = 'hello@helium.com'
packages = ['geckoboard']
requires = [
    "future>=0.15",
    "requests<2.11",
    "iso4217",
]
setup_requires = [
    'vcversioner',
]
with open('README.md', 'r') as infile:
    long_description = infile.read()

setup(
    name='geckoboard-python',
    description='Wrapper for the Geckboboard DataSet API',
    long_description=long_description,
    author=author,
    author_email=author_email,
    url='https://github.com/helium/geckoboard-python',
    packages=packages,
    setup_requires=setup_requires,
    install_requires=requires,
    include_package_data=True,
    license='BSD',
    vcversioner={
        "version_module_paths": ["geckoboard/_version.py"]
    },
)
