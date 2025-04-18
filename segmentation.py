import numpy as np
import tensorflow as tf
from huggingface_hub import hf_hub_download
from PIL import Image
import streamlit as st

@st.cache_resource
def load_segmentation_model():
    return tf.keras.models.load_model("models/model_unet_2d_attention_combineloss.keras", compile=False)

def segment_image(model, img: Image.Image, input_size: int = 128) -> np.ndarray:
    gray = img.convert("L").resize((input_size, input_size))
    arr = np.array(gray, dtype="float32") / 255.0
    inp = np.stack([arr] * 4, axis=-1)[np.newaxis, ...]
    preds = model.predict(inp)
    mask = np.argmax(preds[0], axis=-1).astype(np.uint8)
    return mask