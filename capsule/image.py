import logging

class DockerImage(object):
    """Simple representation of a docker image as defined by the repo and tag fields"""

    client = None

    repo = ""
    tag = ""

    def __init__(self, client, repo, tag):
        self.client = client

        self.repo = repo
        self.tag = tag

    def __repr__(self):
        return self.repo + ":" + self.tag

    def __str__(self):
        return self.repo + ":" + self.tag

    def exists(self):
        """Test whether this image exists in the client"""

        return str(self) in [img for sublist in self.client.images() for img in sublist['RepoTags']]

    def download(self):
        """Download this image using the client"""

        logging.debug("Downloading %s", self)
        [logging.debug(line) for line in self.client.pull(repository=self.repo, tag=self.tag)]

        if self.exists():
            logging.debug("Download complete")
        else:
            logging.error("Something went wrong while downloading %s", self)

    def build(self, dockerfile):
        """Build this image given a dockerfile string"""

        #f = BytesIO(bytes(dockerfile, 'utf-8'))
        #[print(l) for l in client.build(fileobj=f, rm=True, tag=str(self))]
        [logging.debug(line) for line in self.client.build(path=dockerfile, rm=True, tag=str(self))]

    def addtag(self, repo, tag):
        """Give this image another tag"""

        self.client.tag(image=str(self), repository=repo, tag=tag)

        return DockerImage(self.client, repo, tag)
