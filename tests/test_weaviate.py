import os
import pytest
import weaviate

from dotenv import load_dotenv

load_dotenv()


def test_weaviate_connection():
    """
    Test weaviate connection
    """
    weaviate_host = os.getenv("WEAVIATE_HOST")
    weaviate_port = int(os.getenv("WEAVIATE_HTTP_PORT"))
    weaviate_grpc_port = int(os.getenv("WEAVIATE_GRPC_PORT"))

    client = weaviate.connect_to_local(
        host=weaviate_host, port=weaviate_port, grpc_port=weaviate_grpc_port
    )

    assert client is not None
    assert client.is_ready() == True

    client.close()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
