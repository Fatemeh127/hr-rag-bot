from litellm import embedding

def get_embedding(text):
    response = embedding(
        model = "text-embedding-3-small",
        input = text
    )

    return response["data"][0]["embedding"]