import logging

class DockerImage(object):
    """Simple representation of a docker image as defined by the repo and tag fields"""

    def __init__(self, repo, tag, client=None):
        self.repo = repo
        self.tag = tag

        self.client = client

    def __repr__(self):
        return "<DockerImage(" + self.repo + "," + self.tag + ")>"

    def __str__(self):
        return self.repo + ":" + self.tag

    def exists(self, client=None):
        """Test whether this image exists in the docker client"""

        if client is None:
            client = self.client

        return str(self) in [img for sublist in client.images() for img in sublist['RepoTags']]

    def download(self, client=None):
        """Download this image using the docker client"""

        if client is None:
            client = self.client

        logging.debug("Downloading %s", self)
        [logging.debug(line) for line in client.pull(repository=self.repo, tag=self.tag)]

        if self.exists():
            logging.debug("Download complete")
        else:
            logging.error("Something went wrong while downloading %s", self)

    def build(self, dockerfile, client=None):
        """Build this image given a dockerfile string"""

        if client is None:
            client = self.client

        [logging.debug(line) for line in client.build(path=dockerfile, rm=True, tag=str(self))]

    def addtag(self, repo, tag, client=None):
        """Give this image another tag"""

        if client is None:
            client = self.client

        client.tag(image=str(self), repository=repo, tag=tag)

        return DockerImage(client, repo, tag)
