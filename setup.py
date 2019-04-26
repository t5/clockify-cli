from setuptools import setup, find_packages

setup(
    name='clockify_cli',
    version='0.10',
    # py_modules=['clockify_cli'],
    packages=find_packages(include=['clockify_cli']),
    author='Theodore Hu',
    url='https://github.com/t5/clockify-cli',
    install_requires=[
        'click==6.7',
        'certifi==2018.8.13',
        'chardet==3.0.4',
        'click==6.7',
        'idna==2.7',
        'requests>=2.20.0',
        'urllib3==1.23',
    ],
    entry_points='''
        [console_scripts]
        clockify=clockify_cli.clockify_cli:main
   ''', 
)
