from setuptools import setup, find_packages

setup(
    name='httpAlive',
    version='2.0.0',
    description='HttpAlive is a web probing tool designed for discovering alive subdomains and URLs.',
    author='Bande Aashish',
    url='https://github.com/aashishtechsecurity/httpAlive',
    packages=find_packages(),
    install_requires=[
        'requests',
        'httpx',
        'colorama',
        'rich',
    ],
    extras_require={
        'dev': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'httpAlive = httpAlive.httpAlive:main',
        ],
    },
)
