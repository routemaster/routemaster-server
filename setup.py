from setuptools import setup

setup(
    name='routemaster-server',
    install_requires=[
        'SQLAlchemy==0.9.7',
        'Flask==0.10.1',
    ],
    scripts=[
        'server.py',
    ],
)
