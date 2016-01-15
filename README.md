This package is meant to help manage development environments using docker, while providing an interface similar  to that of python's `virtualenvwrapper` module.

**Note:** This code is in alpha stage. You're free to try it out and provide feedback, but keep in mind it will undergo heavy changes before it's production ready.

[![Stories in Ready](https://badge.waffle.io/tryexceptpass/capsule.png?label=ready&title=Ready)](https://waffle.io/tryexceptpass/capsule)

## Features
* Simple cli to create, switch to and delete environments that allow you to fiddle to your heart's content without breaking anything else. 
* Currently this is based on a clean Ubuntu install (`ubuntu:latest` docker [image](https://hub.docker.com/_/ubuntu/)) with basic python 2.7 configured.
* Save your environment to a tarfile in case you want to take it with you anywhere.
* Export the python history of anything you tried while using the python interpreter within your environment into an iPythonNotebook file that can be used with any Jupyter server (like the `jupyter/notebook` docker [image](https://hub.docker.com/r/jupyter/notebook/)).

## Install
1. Setup and install [docker](http://docs.docker.com/linux/started/) or [docker-machine](https://www.docker.com/docker-toolbox) on your computer.
2. `git clone` this repo.
3. `python setup.py install`

## Usage
The setup script installs a `capsule` shell command that provides the interface described below. Any environment you create is essentially a new docker container and will therefore maintain state next time you work on it. The `save` and `load` commands essentially export / import the environment to a tarfile.

The environment is an Ubuntu install with python 2.7 by default (I'll provide a python 3 option soon) and is configured to keep track of your python history when using the interpreter. This allows us to automatically export any experiments you run within the python interpreter to an iPythonNotebook through the `pyhistory` command.

```
Manage capsule environments.

Usage:
  capsule make <name> [options]
  capsule workon <name> [options]
  capsule remove <name> [options]
  capsule list [options]
  capsule save <name> [options]
  capsule load <filename> <name>
  capsule pyhistory <name>

Options:
  --baseimage

  --debug       Print debug messages.
  -h --help     Show this screen.
  --version     Show version.
```

Note: please be patient the first time you run it, as it will take a little bit while we run a docker build to download and create the first container.
