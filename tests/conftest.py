import sys
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)


import os
import logging
from urllib.parse import urlparse

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.core.container import DockerContainer
from testcontainers.core.network import Network
from testcontainers.core.image import DockerImage
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.generic import ServerContainer
from testcontainers.postgres import PostgresContainer

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def docker_network():
    with Network() as network:
        yield network


@pytest.fixture(scope="session")
def psql():
    with PostgresContainer("postgres:14-alpine") as postgres:
        connection_string = urlparse(postgres.get_connection_url())

        with DockerImage(path="./", tag="url-migrations-test:latest") as image:
            with DockerContainer(str(image)).with_env(
                "db_config__user", connection_string.username
            ).with_env("db_config__password", connection_string.password).with_env(
                "db_config__name", connection_string.path.lstrip("/")
            ).with_env(
                "db_config__host",
                os.getenv("DOCKER_IP_FOR_TESTS", "host.docker.internal"),
            ).with_env(
                "db_config__port", str(connection_string.port)
            ).with_command(
                """bash -c "alembic upgrade head && echo 'migrated!'" """
            ) as container:
                delay = wait_for_logs(container, "migrated!")

        yield postgres


@pytest.fixture(scope="session")
def url_app(psql):
    connection_string = urlparse(psql.get_connection_url())

    os.environ['db_config__user'] = connection_string.username
    os.environ['db_config__password'] = connection_string.password
    os.environ['db_config__name'] = connection_string.path.lstrip("/")
    os.environ['db_config__host'] = os.getenv("DOCKER_IP_FOR_TESTS", "localhost")
    os.environ['db_config__port'] = str(connection_string.port)

    from fastapi.testclient import TestClient

    from app.main import create_app
    client = TestClient(create_app())
    yield client


@pytest.fixture(scope="session")
def db_session(psql):
    engine = create_engine(psql.get_connection_url())
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

