from setuptools import setup

setup(
    name="ftc-utils",
    description="Crawlers and db utils",
    version="0.0.1",
    package_dir={"": "src"},
    packages=["data", "scrapy", "selenium"],
    url="https://github.com/bear-trends/ftc-utils",
    author="Smirkey&Anko59",
    author_email="mariedelahouce@gmx.fr",
    keywords=["scraping", "sourcing", "leboncoin", "vinted"],
    include_package_data=True,
)
