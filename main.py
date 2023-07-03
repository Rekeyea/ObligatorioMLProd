from typing import List, Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import uuid
import gradio as gr
from pydantic import BaseModel
from inference import batch_inference, online_inference
from fastapi.staticfiles import StaticFiles
import json
import pandas as pd
import io

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

def process_data_batch(csv_file):
    # Read the CSV file into a Pandas DataFrame
    results = []
    with open(csv_file.name) as fo:
        content = fo.read()
        df = pd.read_csv(io.StringIO(content))

        # Process each line in the DataFrame
        requests = [(row['text'], row['url']) for _,row in df.iterrows()]
        results = batch_inference(requests)
        
        # for _, row in df.iterrows():
        #     text = row['text']
        #     url = row['url']
        #     # Perform your desired processing on each line
        #     # You can modify this code block to perform specific actions on text and URL

        #     # Append the processed result to the list
        #     data = online_inference((text, url))
        #     print(data)
        #     results.append(data)

    return results


demo = gr.Interface(fn=process_data, inputs=["text", "image"], outputs="text")
demo_batch = gr.Interface(fn=process_data_batch, inputs="file", outputs="text", title="CSV Processing Interface")

app = gr.mount_gradio_app(app, demo, path="/dashboard")
app = gr.mount_gradio_app(app, demo_batch, path="/batch")