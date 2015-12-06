from setuptools import setup, find_packages

setup(
    name = "Capsule",
    version = "0.1",
    packages = find_packages(), 

    install_requires = [ 'docopt', 'docker-py' ],

    license = "MIT",

    scripts = ["bin/capsule"]
)