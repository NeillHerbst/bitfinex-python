from setuptools import setup, find_packages

setup(
    name='bitfinex_api',
    version='0.0.1',
    description='package containing the API endpoints of Bitfinex',
    url='https://github.com/NeillHerbst/bitfinex-python.git',
    author='Neill Herbst',
    author_email='n.herbst6@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires = [
        'requests==2.14.2',
        'websocket-client==0.44.0'
    ]
)