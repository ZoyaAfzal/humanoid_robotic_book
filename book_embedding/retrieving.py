import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
cohere_client = cohere.Client("QVVViq3UKczgO0P7QZ302I7xk8JsUmWfrsiEbw4o")

# Connect to Qdrant
qdrant = QdrantClient(
    url="https://fd51812c-3541-4d56-aa03-7db87f4beba4.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ha03izlu7nPCmVy74eZr20UOmEVQiCIQ3TaFx03zhNQ",
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

def retrieve(query):
    embedding = get_embedding(query)
    # Determine the correct search method by trying each one in order of preference
    result = None
    last_exception = None

    # Try the most modern method first
    try:
        result = qdrant.search(
            collection_name="humanoid_robotic_book",
            query_vector=embedding,
            limit=5
        )
    except AttributeError as e:
        last_exception = e
    except Exception as e:
        last_exception = e

    # If search failed, try search_points (older method)
    if result is None:
        try:
            result = qdrant.search_points(
                collection_name="humanoid_robotic_book",
                vector=embedding,
                limit=5
            )
        except AttributeError as e:
            last_exception = e
        except Exception as e:
            last_exception = e

    # If both failed, try query_points (another version)
    if result is None:
        try:
            result = qdrant.query_points(
                collection_name="humanoid_robotic_book",
                query=embedding,
                limit=5
            )
        except AttributeError as e:
            last_exception = e
        except Exception as e:
            last_exception = e

    # If all methods failed, raise an error
    if result is None:
        raise last_exception or AttributeError("Qdrant client does not have a recognized search method.")
    return [point.payload["text"] for point in result.points]

# Test
print(retrieve("What data do you have?"))