from http.client import HTTPResponse
from typing import Callable, List, Union, Annotated
from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from authentication import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, Token, TokenData, User, authenticate_user, create_access_token, get_current_user, get_user, oauth2_scheme

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

import time
from fastapi.routing import APIRoute

import gradio as gr
from pydantic import BaseModel

from inference import batch_inference, online_inference, text_embedding

import json

app = FastAPI()

class TextImageRequest(BaseModel):
    text: str
    url: str

@app.get("/")
async def test():
    return {"Hello": "World"}

@app.post("/embeddings/text")
async def embeddings_text_api(request: TextImageRequest):
    return text_embedding(request.text)

@app.post("/inference/online")
def inference_text_api(request: TextImageRequest):
    return online_inference((request.text, None))

@app.post("/inference/batch")
def inference_text_api(request: List[TextImageRequest]):
    res = batch_inference([(r.text, None) for r in request])
    return res

@app.get("/logs/classifications")
def get_classifications():
    result = []

    with open("./log.txt", 'r') as file:
        for line in file:
            # Transform each line into a dictionary
            data = json.loads(line)
            result.append(data)

    return result


def process_data(text, image):
    return online_inference((text, image))

demo = gr.Interface(fn=process_data, inputs=["text", "image"], outputs="text")

app = gr.mount_gradio_app(app, demo, path="/dashboard")