import os
import pytest
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI


def test_openai_chat_response():
    """
    Test chat response from OpenAI
    """
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="You are a coding assistant that talks like a pirate.",
        input="How do I check if a Python object is an instance of a class?",
    )

    assert response is not None
    assert response.output[0].content is not None
    assert len(response.output[0].content[0].text.strip()) > 0


def test_openai_embedding_response():
    """
    Test embedding response from OpenAI
    """
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="Hello, how are you?",
    )

    assert response is not None
    assert response.data[0].embedding is not None
    assert len(response.data[0].embedding) > 0


if __name__ == "__main__":
    pytest.main([__file__])
