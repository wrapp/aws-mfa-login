from setuptools import setup

setup(
    name = "aws-mfa-auth",
    version = "1.0.0",
    packages = ['wrapp', 'wrapp.aws'],
    author = "Fredrik Håård",
    author_email = "fredrik@metallapan.se",
    description = "Generates environment variables for MFA auth against AWS CLI",
    license = "MIT",
    keywords = "aws mfa cli",
    url = "https://github.com/wrapp/aws-mfa-auth",
    classifiers = """Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: Freely Distributable
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 3""".split('\n'),
    long_description = open('README.md', 'rt').read(),
    entry_points = {
        'console_scripts': [
            'aws-mfa-auth = wrapp.aws.mfa:main',
            'ama = wrapp.aws.mfa:main',
            ]
        },
)
