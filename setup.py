from setuptools import setup

setup(
    name='rm-server',
    install_requires=[
        'SQLAlchemy==0.9.7',
        'Flask==0.10.1',
        'docopt==0.6.2',
        'tornado==4.0.2',
    ],
    packages=[
        'routemaster',
    ],
    scripts=[
        'server.py',
    ],
)
