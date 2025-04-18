import tensorflow as tf
from huggingface_hub import hf_hub_download
import numpy as np
from PIL import Image
import streamlit as st

@st.cache_resource
def load_segmentation_model():
    model_file = hf_hub_download(
        repo_id="AndyWu0719/unet2dattentionmodel",
        filename="model_unet_2d_attention_combineloss.keras"
    )
    return tf.keras.models.load_model(model_file, compile=False)

def segment_image(model, image: Image.Image) -> np.ndarray:
    input_size = 128
    img_gray = image.convert("L")
    img_resized = img_gray.resize((input_size, input_size))
    arr_single = np.array(img_resized, dtype="float32") / 255.0
    arr = np.stack([arr_single] * 4, axis=-1)
    arr = arr[np.newaxis, ...]
    preds = model.predict(arr)
    mask = np.argmax(preds[0], axis=-1).astype(np.uint8)
    return mask