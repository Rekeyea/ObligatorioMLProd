import numpy as np
from PIL import Image
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def converToRGB(image):
    if image is None: 
        image = Image.new("RGB", (299, 299), (0,0,0))
    if image.mode == 'RGBA':
        # Create a new RGB image with a white background
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        # Composite the RGBA image onto the RGB image
        rgb_image.paste(image, mask=image.split()[3])
        return rgb_image
    elif image.mode == 'RGB':
        # If the image is already in RGB format, return it as it is
        return image
    else:
        # For other image modes, convert to RGB
        return image.convert('RGB')

def preProcessPredictImage(image):
    image = converToRGB(image)
    image = image.resize((299, 299))
    image = np.array(image)
    image = tf.keras.applications.xception.preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image


def preProcessPredictText(text):
    # Convert the text to a numerical representation using a tokenizer
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([text])
    numerical_text = tokenizer.texts_to_sequences([text])[0]
    # Pad the numerical text sequence to have a length of 20
    padded_text = pad_sequences([numerical_text], maxlen=20)
    # Remove the extra dimension
    padded_text = tf.squeeze(padded_text, axis=0)
    tensor = tf.convert_to_tensor([padded_text])
    return tensor

def preProcessTextAndImage(text, image):
    precText = preProcessPredictText(text)
    precImage = preProcessPredictImage(image)
    return [precImage, precText]