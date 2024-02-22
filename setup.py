from setuptools import setup, find_packages

setup(
    name = "scraper",
    version = "0.1.1",
    packages = find_packages(),
    include_package_data = True,
    py_modules = [
        'scraper',
    ],
    install_requires = [
        'bs4',
        'lxml',
        'Pillow',
        'click',
        'python-dotenv',
        'requests',
    ],
    entry_points = {
        "console_scripts" : [
            "scraper = scraper:scraper",
        ],
    }
)