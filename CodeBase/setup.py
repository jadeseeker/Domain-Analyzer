from setuptools import setup, find_packages


setup(
    name = 'blackthread',
    version = '0.1',
    url = 'https://github.gatech.edu/agupta402/BlackThread',
    description = 'Program that parses a website\'s content and analyzes it for changes.',
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['blackthread = tags.crawl:main']
    },
    zip_safe = True,
    install_requires=[
        'scrapy>=0.24.4',
        'twisted>=14.0.2',
        'pyasn1>=0.1.7',
        'service-identity>=14.0.0',
        'beautifulsoup4>=4.3.2',
        'stop-words>=2014.5.26'
    ]
)
