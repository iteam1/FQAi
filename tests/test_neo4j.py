import os
import pytest

from dotenv import load_dotenv

load_dotenv()

from neo4j import GraphDatabase


def test_neo4j_connection():
    """
    Test neo4j connection

    URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
    """
    is_connected = False
    neo4j_uri = os.getenv("NEO4J_URI") + os.getenv("NEO4J_HOST")
    auth = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

    with GraphDatabase.driver(neo4j_uri, auth=auth) as driver:
        try:
            driver.verify_connectivity()
            is_connected = True
        except Exception as e:
            is_connected = False

    assert is_connected


if __name__ == "__main__":
    pytest.main(["-v", __file__])
