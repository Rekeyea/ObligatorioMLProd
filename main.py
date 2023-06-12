from typing import List, Union, Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from authentication import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, Token, TokenData, User, authenticate_user, create_access_token, get_current_user, get_user, oauth2_scheme
from inference import ImageRequest, TextRequest, online_inference_img, online_inference_text

app = FastAPI()

@app.get("/")
async def test():
    return {"Hello": "World"}

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/inference/text")
async def inference_text_api(request: TextRequest):
    return online_inference_text(request)


@app.post("/inference/img")
def inference_text_api(request: ImageRequest):
    return online_inference_img(request)


@app.post("/inference/batch")
def inference_text_api(request: List[ImageRequest | TextRequest]):
    return online_inference_img(request)