import pytest
from ollama import generate, chat, embed
from ollama import ChatResponse


def test_ollama_generate_response():
    """
    Test generate response from Ollama
    """
    response = generate("deepseek-r1:1.5b", "Why is the sky blue?")
    assert response is not None
    assert "response" in response
    assert len(response["response"].strip()) > 0


def test_ollama_chat_response():
    """
    Test chat response from Ollama
    """
    response: ChatResponse = chat(
        model="deepseek-r1:1.5b",
        messages=[
            {
                "role": "user",
                "content": "Hello, how are you?",
            },
        ],
    )

    # Assert response is not None
    assert response is not None

    # Assert response has message content
    assert "message" in response
    assert "content" in response["message"]

    # Assert content is not empty
    content = response["message"]["content"]
    assert content is not None
    assert len(content.strip()) > 0


def test_ollama_embedding_response():
    """
    Test embedding response from Ollama
    """
    response = embed(model="embeddinggemma:latest", input="Hello, how are you?")

    # Assert response is not None
    assert response is not None

    # Assert response has embeddings content
    assert "embeddings" in response
    assert len(response["embeddings"]) > 0


if __name__ == "__main__":
    pytest.main(["-v", __file__])
