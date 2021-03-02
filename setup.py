from setuptools import setup

setup(
    name='telegramegle',
    version='1.0.0',
    url='https://github.com/AlessioPlease/telegramegle',
    license='MIT',
    author='Alessio',
    author_email='none',
    description='Python API for Omegle chat and Telegram bot',
    packages=[ 'pyomegle' ],
    install_requires=[ 'mechanize','Levenshtein' ]
)
