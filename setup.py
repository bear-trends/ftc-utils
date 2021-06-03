from setuptools import setup

setup(
    name="ftc-utils",
    description="Crawlers and db utils",
    version="0.0.3",
    packages=[
        "ftc_utils",
        "ftc_utils.data",
        "ftc_utils.scrapy",
        "ftc_utils.selenium",
    ],
    url="https://github.com/bear-trends/ftc-utils",
    author="Smirkey&Anko59",
    author_email="mariedelahouce@gmx.fr",
    keywords=["scraping", "sourcing", "leboncoin", "vinted"],
    include_package_data=True,
)
