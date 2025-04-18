from huggingface_hub import hf_hub_download
import os

model_path = hf_hub_download(
    repo_id="AndyWu0719/unet2dattentionmodel",
    filename="model_unet_2d_attention_combineloss.keras",
    local_dir="models",
    local_dir_use_symlinks=False
)