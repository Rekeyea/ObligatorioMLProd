from http.client import HTTPResponse
from typing import Callable, List, Optional, Union, Annotated
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
import uuid

import time
from fastapi.routing import APIRoute

import gradio as gr
from pydantic import BaseModel

from inference import batch_inference, online_inference, text_embedding

from fastapi.staticfiles import StaticFiles

import json

from PIL import Image

environment = os.environ.get('ENVIRONMENT', 'development')
print(environment)
if environment == 'production':
    # Load production configuration
    from config.production import HOST
else:
    # Load development configuration (default)
    from config.development import HOST

print(f"************* {HOST} ***************")


app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

class TextImageRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

@app.get("/")
async def test():
    return {"Hello": "World"}

@app.post("/inference/online")
def inference_text_api(request: TextImageRequest):
    return online_inference((request.text, request.url))

@app.post("/inference/batch")
def inference_text_api(request: List[TextImageRequest]):
    res = batch_inference([(r.text, r.url) for r in request])
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
    image_url = None
    if image is not None:
        pil_image = Image.fromarray(image)
        random_filename = str(uuid.uuid4()) + '.jpg'
        save_directory = './public'
        save_path = os.path.join(save_directory, random_filename)
        pil_image.save(save_path)
        image_url = f"{HOST}/public/{random_filename}"
    return online_inference((text, image_url))

demo = gr.Interface(fn=process_data, inputs=["text", "image"], outputs="text")

app = gr.mount_gradio_app(app, demo, path="/dashboard")