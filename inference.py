from typing import List
from pydantic import BaseModel
from embeddings import generate_embedding

class TextRequest(BaseModel):
    text: str

class ImageRequest(BaseModel):
    url: str

def text_embedding(request: TextRequest):
    embeddings = generate_embedding(request.text)
    return {"embeddings": embeddings}

def online_inference_text(request: TextRequest):
    print(request)
    return {"category": 1}

def online_inference_img(request: ImageRequest):
    print(request)
    return {"category": 1}

def batch_inference(request: List[TextRequest | ImageRequest]):
    print(request)
    return [{"category": 1}]
