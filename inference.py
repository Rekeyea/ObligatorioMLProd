from typing import List, Tuple
from PIL import Image
from logger_decorator import log_decorator, log_decorator_batch
import requests
from io import BytesIO
from keras.models import load_model
import numpy as np

from processing import preProcessTextAndImage

model = load_model('./model/model.h5')

def get_image(url):
    if url is None:
        return None
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

@log_decorator
def online_inference(request: Tuple[str, str]):
    (text, image_url) = request
    image = get_image(image_url)
    tensor = preProcessTextAndImage(text, image)
    predictions = model.predict(tensor)
    return {"prediction": f"Store {np.argmax(predictions[0]).item() + 1}"}

@log_decorator_batch
def batch_inference(request: List[Tuple[str | None, str | None]]):
    actual_inputs = [(text, get_image(url)) for (text, url) in request]
    tensors = [preProcessTextAndImage(text, image) for (text, image) in actual_inputs]
    predictions = [model.predict(tensor) for tensor in tensors]
    print(predictions)
    return [{"prediction": f"Store {np.argmax(prediction[0]).item() + 1}"} for prediction in predictions]
