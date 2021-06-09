import docker


class DockerClientService:

    def __init__(self):
        self.client = docker.from_env()
