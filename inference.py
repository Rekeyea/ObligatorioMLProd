from typing import List, Tuple
from PIL import Image
from embeddings import generate_embedding
from logger_decorator import log_decorator, log_decorator_batch

def text_embedding(text: str):
    embeddings = generate_embedding(text)
    return {"embeddings": embeddings}

@log_decorator
def online_inference(request: Tuple[str, str]):
    print(f"ONLINE {request}")
    (text, image) = request
    return {"category": 1}

@log_decorator_batch
def batch_inference(request: List[Tuple[str, str]]):
    print(f"BATCH {request}")
    print(len(request))
    return [{"category": 1} for r in request]
