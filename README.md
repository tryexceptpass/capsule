This package is meant to help manage development environments using docker, while providing an interface similar  to that of python's `virtualenvwrapper` module.

**Note:** This code is in alpha stage. You're free to try it out and provide feedback, but keep in mind it will undergo heavy changes before it's production ready.

## Features
* Simple cli to create, switch to and delete environments that allow you to fiddle to your heart's content without breaking anything else. 
* Currently this is based on a clean Ubuntu install (`ubuntu:latest` docker [image](https://hub.docker.com/_/ubuntu/)) with basic python 2.7 configured.
* Save your environment to a tarfile in case you want to take it with you anywhere.
* Export the python history of anything you tried while using the python interpreter within your environment into an iPythonNotebook file that can be used with any Jupyter server (like the `jupyter/notebook` docker [image](https://hub.docker.com/r/jupyter/notebook/)).

## Install
1. Setup and install [docker](http://docs.docker.com/linux/started/) or [docker-machine](https://www.docker.com/docker-toolbox) on your computer.
2. `git clone` this repo.
3. `pip install -r requirements.txt`

## Usage
The repo comes with a symlink `cenv` to `capsulenv.py` to reduce typing, however once I complete a setup.py script, the idea is to install this as a `capsule` command in your OS.

```
Manage capsule environments.

Usage:
  capsulenv make <name> [options]
  capsulenv workon <name> [options]
  capsulenv remove <name> [options]
  capsulenv list [options]
  capsulenv save <name> [options]
  capsulenv load <filename> <name>
  capsulenv pyhistory <name>

Options:
  --baseimage

  --debug       Print debug messages.
  -h --help     Show this screen.
  --version     Show version.
```
