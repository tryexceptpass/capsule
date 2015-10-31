from docker.utils import create_host_config

import logging
import subprocess

import io

class DockerContainer(object):
    """Simple representation of a docker container as defined by a name and parent image"""

    client = None

    image = None
    name = ""
    config = None
    container = None

    def __init__(self, client, image, name):
        self.client = client
        self.image = image
        self.name = name

    def __repr__(self):
        return "%s<%s>" % (self.name, str(self.image))

    def __str__(self):
        return "%s<%s>" % (self.name, str(self.image))

    def link(self, config):
        self.config = create_host_config(links=config)

    def run(self, command='/bin/bash'):
        status = None
        create = True

        if self.container:
            container = self._findcontainerbyid(self.container['Id'])
            # status = container['Status']
            # create = False
            # logging.debug("Container %s already exists", self.name)

            # for container in self.client.containers(all=True):
            #     if container['Id'] == self.container['Id']:
            #         status = container['Status']
            #         create = False
            #         logging.debug("Container %s already exists", self.name)
            #         break
        else:
            container = self._findcontainerbyname(self.name)

        if container is not None:
            self.container = container
            status = container['Status']
            # create = False
            logging.debug("Container %s already exists", self.name)

            # for container in self.client.containers(all=True):
            #     if '/' + self.name in container['Names']:
            #         self.container = container
            #         status = container['Status']
            #         create = False
            #         logging.debug("Container %s already exists", self.name)
        else:
            if self.config:
                self.container = self.client.create_container(name=self.name, command=command, image=str(self.image), tty=True, stdin_open=True, host_config=self.config)
            else:
                self.container = self.client.create_container(name=self.name, command=command, image=str(self.image), tty=True, stdin_open=True)
            logging.debug("Container %s built from %s image", self.name, str(self.image))

        if status is None:
            self.start()
        elif 'Exited' in status:
            self.restart()

        logging.debug("Started %s", self.name)

    def _findcontainerbyname(self, name):
        for container in self.client.containers(all=True):
            if '/' + name in container['Names']:
                return container

        return None

    def _findcontainerbyid(self, id):
        for container in self.client.containers(all=True):
            if id == self.container['Id']:
                return container

        return None

    def inspect(self):
        return self.client.inspect_container(container=self.name)

    def stop(self, timeout=10):
        self.client.stop(container=self.container['Id'], timeout=timeout)

    def remove(self, volumes=True, force=True):
        if self.container is None:
            container = self._findcontainerbyname(self.name)

            if container:
                self.container = container
            else:
                return

        self.client.remove_container(container=self.container['Id'], force=force, v=volumes)

    def restart(self):
        self.client.restart(container=self.container['Id'])

    def start(self):
        self.client.start(container=self.container['Id'])

    def attach(self):
        subprocess.Popen(['docker', 'attach', self.container['Id']]).communicate()

    def copy(self, resource):
        if (self.container is None):
            self.run()

        return io.BytesIO(self.client.copy(container=self.container['Id'], resource=resource).read(cache_content=False))
    