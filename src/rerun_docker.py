import time
import docker
from docker.models.containers import Container

client = docker.from_env()


def check_container(name: str) -> bool:
    '''
    Check if a container with the given name exists.

    Parameters
    ----------
    name: str
        The name of the container to check.

    Returns
    -------
    bool
        True if the container exists, False otherwise.
    '''
    containters = [
        container.name
        for container in client.containers.list()
    ]
    return name in containters


def ensure_container_remove(container: Container) -> None:
    """
    Remove given container and wait until it is removed.

    Parameters
    ----------
    container: Container
        The container to remove.
    """
    container.stop()
    if not container.attrs["HostConfig"]["AutoRemove"]:
        container.remove(force=True)
    if container.name is not None:
        while check_container(container.name):
            time.sleep(1)


def reload_docker_container(name: str, **kwargs) -> Container:
    '''
    Create container, in case it already created - remove it and create
    new one.

    Parameters
    ----------
    name: str
        The name of the container to create or remove.
    kwargs: dict
        All other keywords for docker.client.containers.run() method.

    Returns
    -------
    Container
        The created container.
    '''

    if check_container(name):
        container = client.containers.get(name)
        ensure_container_remove(container)

    return client.containers.run(
        name=name,
        **kwargs
    )
