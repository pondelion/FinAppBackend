from setuptools import setup, find_packages

setup(
    name='fin_app',
    version='0.1.0',
    description='FinAppBackend',

    author='pondelion',
    url='https://github.com/pondelion/FinAppBackend',

    packages=find_packages(where='fin_app'),
    package_dir={'': 'fin_app'},

    install_requires=[],
    extras_require={},

    entry_points={
        'console_scripts': [
            'fin_app = fin_app'
        ]
    },
)