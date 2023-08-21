from setuptools import setup

""" python = "^3.9"
weasyprint = "^52.5"
bs4 = "^0.0.1"
progress = "^1.6"
geopandas = "^0.9.0"
contextily = "^1.1.0"
matplotlib = "^3.4.2"""

setup(
    name='PrintMyReport',
    version='0.0.3',
    install_requires=[
        'weasyprint',
        'bs4',
        'progress',
        'geopandas',
        'contextily',
        'matplotlib',
        "matplotlib-scalebar",
    ],
)

