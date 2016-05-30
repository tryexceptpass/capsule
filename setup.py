from setuptools import setup, find_packages

setup(
    author = "tryexceptpass",
    author_email = "tryexceptpass@users.noreply.github.com",

    name = "capsule",
    version = "0.2.1",
    description = "Manage development environments like virtualenv but with docker containers and export your python history to iPythonNotebook",
    long_description="This package is meant to help manage development environments using docker, while providing an interface similar to that of python's virtualenvwrapper module.\n\nFeatures:\n\n* Simple cli to create, switch to and delete environments that allow you to fiddle to your heart's content without breaking anything else.\n\n* Currently this is based on a clean Ubuntu install (ubuntu:latest docker image) with basic python 2.7 configured.\n\n* Save your environment to a tarfile in case you want to take it with you anywhere.\n\n* Export the python history of anything you tried while using the python interpreter within your environment into a JupyterNotebook file that can be used with any Jupyter server (like the jupyter/notebook docker image).",

    url = "https://github.com/tryexceptpass/capsule",

    packages = find_packages(),

    install_requires = [ 'docopt', 'docker-py' ],

    license = "MIT",
    classifiers = [ 'License :: OSI Approved :: MIT License',

                    'Topic :: Software Development',
                    'Topic :: Scientific/Engineering',
                    'Topic :: System',
                    'Topic :: Software Development :: Testing',
                    'Topic :: Utilities',

                    'Development Status :: 4 - Beta',

                    'Framework :: IPython',
                  ],
    keywords = [ 'docker', 'virtualenv', 'environments', 'ipynb', 'ipythonnotebook', 'jupyternotebook' ],

    scripts = ["bin/capsule"]
)
