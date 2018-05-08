from setuptools import setup

setup(
    name="aws-mfa-login",
    version="1.0.1",
    packages=['wrapp', 'wrapp.aws'],
    author="Joakim Lundborg, Fredrik Håård",
    author_email="joakim.lundborg@wrapp.com, fredrik@metallapan.se",
    description="Generates environment variables for MFA auth against AWS CLI. Python 3.3+.",
    license="MIT",
    keywords="aws mfa cli",
    url="https://github.com/wrapp/aws-mfa-login",
    classifiers="""Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: Freely Distributable
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3""".split('\n'),
    long_description=open('README.md', 'rt').read(),
    entry_points={
        'console_scripts': [
            'aws-mfa-login = wrapp.aws.mfa:main',
            'aml = wrapp.aws.mfa:main',
        ]
    },
)
