from setuptools import setup

setup(
    name="find-the-cheapest",
    description="Scraper repo and more",
    version="0.0.1",
    package_dir={"": "src"},
    packages=["leboncoin_selenium", "vinted_selenium", "ebay_selenium", "ftc_utils"],
    url="https://github.com/Smirkey/find-the-cheapest",
    author="Smirkey&Anko59",
    author_email="mariedelahouce@gmx.fr",
    keywords=["scraping", "sourcing", "leboncoin", "vinted"],
    include_package_data=True,
)
