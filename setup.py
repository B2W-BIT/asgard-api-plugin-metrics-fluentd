from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='asgard-api-plugin-metrics-fluentd',
    version='0.1.1',

    description='Asgard API endpoints to get Fluentd metrics',
    long_description="Plugin para a Asgard API e que fornece métricas do cluster de Fluentd",
    url='https://github.com/B2W-BIT/asgard-api-plugin-metrics-fluentd',
    # Author details
    author='Dalton Barreto',
    author_email='daltonmatos@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires = [
        "asgard-api-sdk>=0.2.0",
        "python-dateutil==2.7.3",
        "requests>=2.0.0",
        "freezegun==0.3.10",
        "pytz==2018.04",
    ],

    entry_points={
        'asgard_api_metrics_mountpoint': [
            'init = fluentdmetrics.plugin:asgard_api_plugin_init',
        ],
    },
)
