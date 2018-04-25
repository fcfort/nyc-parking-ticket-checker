# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nyc-parking-ticket-checker',  # Required
    version='0.0.6',  # Required
    description='A module to query for NYC parking tickets',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/fcfort/nyc-parking-ticket-checker',  # Optional
    author_email='frank.c.fort@gmail.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        # Specify the Python versions you support here.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ticket plates violation-number nyc',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=[
        'BeautifulSoup4',
        'mechanize',
    ],

    entry_points={  # Optional
        'console_scripts': [
            'ticket_checker=nycparkingticket.ticket_checker:main',
        ],
    },
)
