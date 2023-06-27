from typing import List, Tuple
from PIL import Image
from embeddings import generate_embedding
from logger_decorator import log_decorator, log_decorator_batch
import requests
from io import BytesIO

def text_embedding(text: str):
    embeddings = generate_embedding(text)
    return {"embeddings": embeddings}

def get_image(url):
    if url is None:
        return None
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

@log_decorator
def online_inference(request: Tuple[str, str]):
    print(f"ONLINE {request}")
    (text, image_url) = request
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return {"category": 1}

@log_decorator_batch
def batch_inference(request: List[Tuple[str | None, str | None]]):
    print(f"BATCH {request}")
    actual_inputs = [(text, get_image(url)) for (text, url) in request]
    return [{"category": 1} for r in actual_inputs]
