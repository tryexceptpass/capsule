"""Capsule helps create isloated development environments using Docker containers"""

from docker import Client
from docker.utils import kwargs_from_env

from .image import DockerImage
from .container import DockerContainer

import logging
import subprocess

import tarfile
import json

class Capsule(object):
    baseimage = None
    environment = None

    client = None

    def __init__(self, name, baseimage="capsule", basetag="base"):
        """Make a new capsule environment"""

        logging.debug("Initializing")

        self.client = Client(**kwargs_from_env(assert_hostname=False))
        logging.debug("Connected client to docker socket")

        self.baseimage = DockerImage(self.client, baseimage, basetag)

        if name is None:
            return
            
        if self.baseimage.exists():
            logging.info("Latest image is already stored locally")
        else:
            baseos = DockerImage(self.client, 'ubuntu', 'latest')
            if baseos.exists():
                #self.baseimage = baseos.addtag('capsule', 'base')
                self.baseimage.build(".")
            else:
                logging.info("Latest image does not exist locally, will have to download")
                baseos.download()
                logging.debug("Image downloaded")
                self.baseimage.build(".")
                #self.baseimage = baseos.addtag('capsule', 'base')

        self.environment = DockerContainer(self.client, self.baseimage, name)

    def start(self):
        """Start this capsule environment"""

        self.environment.run()

    def stop(self):
        """Stop this capsule environment"""

        self.environment.stop()

    def remove(self):
        """Remove this capsule environment"""

        self.environment.remove()

    def activate(self):
        """Opens the environment for work"""

        self.environment.attach()

    def list(self):
        """List available capsule environments"""

        capsules = []
        containers = self.client.containers(all=True)
        for container in containers:
            if container['Image'] == str(self.baseimage):
                capsules.append(container['Names'][0][1:])

        return capsules

    def pyhistory(self):
        """Get python history for this capsule"""

        tar = tarfile.open(fileobj=self.environment.copy("/root/.pyhistory"))
        cells = []
        for line in str(tar.extractfile(".pyhistory").read(), 'utf-8').split('\n'):
            cells.append({  "cell_type": "code",
                            "execution_count": None,
                            "metadata": { "collapsed": True },
                            "outputs": [],
                            "source": [ line ]
                        })

        ipynb = {   "cells": cells,
                    "metadata": {
                        "kernelspec": {
                            "display_name": "Python 2",
                            "language": "python",
                            "name": "python2"
                        },
                        "language_info": {
                            "codemirror_mode": {
                                "name": "ipython",
                                "version": 2
                            },
                            "file_extension": ".py",
                            "mimetype": "text/x-python",
                            "name": "python",
                            "nbconvert_exporter": "python",
                            "pygments_lexer": "ipython2",
                            "version": "2.7.6"
                        }
                    },
                    "nbformat": 4,
                    "nbformat_minor": 0
                }

        with open(self.environment.name + ".ipynb", 'wb') as f:
            f.write(bytes(json.dumps(ipynb), 'utf-8'))
