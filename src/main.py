from fastapi import FastAPI
from routers import answer
from configs import get_session_with_headers
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchText
from qdrant_client.http.models import Distance, VectorParams

app = FastAPI()

app.include_router(answer.router)

client = QdrantClient("localhost", port=6333)
COLLECTION_NAME = 'test_collection'

# client.create_collection(collection_name="test_collection",
#                          vectors_config=VectorParams(size=4, distance=Distance.DOT))


def embed_text(text: List[str]):
    session = get_session_with_headers()
    payload = {
        "model": "text-embedding-3-small",
        "input": text,
        "dimensions": 4
    }
    response = session.post(
        "https://api.openai.com/v1/embeddings", json=payload)

    vector_of_text = [item['embedding']
                      for item in response.json()["data"]]
    return map_text_with_vector(text, vector_of_text)


def map_text_with_vector(text, vector_of_text):
    points = [{"vector": vector, "text": text}
              for text, vector in zip(text, vector_of_text)]
    return points


SAMPLE_PICKUP_LINES = ['Are you a magician? Because whenever I look at you, everyone else disappears.',
                       'Do you have a map? I keep getting lost in your eyes.', "Do you have a name, or can I call you mine?", "Do you have a name, or can I call you mine?"]
SAMPLE_DISSING_LINES = ["why you're so ugly", "you look like a toothpick",
                        "you are so idiot", "your smell is so digusting"]

sample_text_with_vector = embed_text(SAMPLE_DISSING_LINES)
print(sample_text_with_vector, 'sample')

question_with_vector = embed_text(
    ['I need to offend someone'])
print(question_with_vector, 'question')

operation_info = client.upsert(
    collection_name=COLLECTION_NAME,
    wait=True,
    points=[
        PointStruct(id=index, vector=value['vector'], payload={
            "quote": value["text"]}) for index, value in enumerate(sample_text_with_vector)
    ]
)

search_result = client.search(collection_name="test_collection",
                              query_vector=question_with_vector[0]["vector"], limit=3)
[print(item.payload) for item in search_result]
