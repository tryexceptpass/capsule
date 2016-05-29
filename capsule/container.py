from docker.utils import create_host_config

import logging
import subprocess

import io

class DockerContainer(object):
    """Simple representation of a docker container as defined by a name and parent image"""

    def __init__(self, image, name, config=None, client=None):
        self.image = image
        self.name = name
        self.client = client

        self.container = None
        self.config = None

    def __repr__(self):
        return "<DockerContainer(" + self.name + "," + str(self.image) + ")>"

    def __str__(self):
        return self.name + "<" + str(self.image) + ">"

    def sethostconfig(self, **kwargs):
        """Set the host configuration when creating this container. Keyword arguments include:
             * binds: bind host directory to container.
             * links: link to another container.
             * port_bindings: expose container ports to the host.
             * lxc_conf
             * priviledged
             * dns
             * volumes_from
             * network_mode: bridge, none, container[id|name] or host.
             * restart_policy
             ...
        There are several more at https://docker-py.readthedocs.io/en/stable/hostconfig/
        """

        self.config = create_host_config(kwargs)

    def run(self, command='/bin/bash', client=None):
        """Run the container and, if provided, execute the command"""

        if client is None:
            client = self.client

        status = None
        container = None

        if self.container:
            container = self._findcontainerbyid(self.container['Id'])
        else:
            container = self._findcontainerbyname(self.name)

        if container is not None:
            self.container = container
            status = container['Status']
            logging.debug("Container %s already exists", self.name)
        else:
            if self.config:
                self.container = client.create_container(name=self.name, command=command, image=str(self.image), tty=True, stdin_open=True, host_config=self.config)
            else:
                self.container = client.create_container(name=self.name, command=command, image=str(self.image), tty=True, stdin_open=True)
            logging.debug("Container %s built from %s image", self.name, str(self.image))

        if status is None:
            self.start()
        elif 'Exited' in status:
            self.restart()

        logging.debug("Started %s", self.name)

    def _findcontainerbyname(self, name, client=None):
        if client is None:
            client = self.client

        for container in client.containers(all=True):
            if '/' + name in container['Names']:
                return container

        return None

    def _findcontainerbyid(self, ident, client=None):
        if client is None:
            client = self.client

        for container in client.containers(all=True):
            if ident == container['Id']:
                return container

        return None

    def inspect(self, client=None):
        """Retrieve a dictionary with container details"""

        if client is None:
            client = self.client

        return client.inspect_container(container=self.name)

    def stop(self, timeout=10, client=None):
        """Stop a running container"""

        if client is None:
            client = self.client

        client.stop(container=self.container['Id'], timeout=timeout)

    def remove(self, volumes=True, force=True, client=None):
        """Remove the container"""

        if client is None:
            client = self.client

        if self.container is None:
            container = self._findcontainerbyname(self.name)

            if container:
                self.container = container
            else:
                return

        client.remove_container(container=self.container['Id'], force=force, v=volumes)

    def restart(self, client=None):
        """Restart the running container"""

        if client is None:
            client = self.client

        client.restart(container=self.container['Id'])

    def start(self, client=None):
        """Start the container"""

        if client is None:
            client = self.client

        client.start(container=self.container['Id'])

    def attach(self):
        """Attach to the running container"""

        subprocess.Popen(['docker', 'attach', self.container['Id']]).communicate()

    def copy(self, resource, client=None):
        """Copy the container"""

        if client is None:
            client = self.client

        if (self.container is None):
            self.run()

        return io.BytesIO(client.copy(container=self.container['Id'], resource=resource).read(cache_content=False))
