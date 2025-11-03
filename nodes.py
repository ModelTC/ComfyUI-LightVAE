"""
LightX2V VAE Nodes for ComfyUI
VAE Loader + 各类 VAE 的 Decode 节点
"""

import os
import torch
import folder_paths
from lightx2v.models.video_encoders.hf.wan.vae import WanVAE
from lightx2v.models.video_encoders.hf.wan.vae_2_2 import Wan2_2_VAE
from lightx2v.models.video_encoders.hf.wan.vae_tiny import WanVAE_tiny, Wan2_2_VAE_tiny

class VAEDecoderLoader:
    @classmethod
    def INPUT_TYPES(cls):
        vae_default_dir = "./models/vae/"
        return {
            "required": {
                "vae_filename": (folder_paths.get_filename_list("vae") ,{"default": "Wan2.1_VAE.safetensors"}),
                "dtype": (["bfloat16", "float16", "float32"], {"default": "bfloat16"}),
                "device": (["cuda", "cpu"], {"default": "cuda"}),
            }
        }
    
    RETURN_TYPES = ("VAE",)
    RETURN_NAMES = ("vae",)
    FUNCTION = "load_vae"
    CATEGORY = "LightX2V"
    
    def load_vae(self, vae_filename: str, dtype: str, device: str):
        dtype_map = {
            "bfloat16": torch.bfloat16,
            "float16": torch.float16,
            "float32": torch.float32
        }
        vae_name = os.path.splitext(vae_filename)[0]
        torch_dtype = dtype_map[dtype]
        vae_path = folder_paths.get_full_path("vae", vae_filename)
        
        if not os.path.exists(vae_path):
            raise FileNotFoundError(f"VAE model not found: {vae_path}")

        if vae_name == "Wan2.1_VAE":
            model = WanVAE(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device,
                use_lightvae=False
            )
            
        elif vae_name == "Wan2.2_VAE":
            model = Wan2_2_VAE(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device
            )
            
        elif vae_name == "lightvaew2_1":
            model = WanVAE(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device,
                use_lightvae=True
            )
            
        elif vae_name == "taew2_1":
            model = WanVAE_tiny(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device,
                need_scaled=False
            ).to(device)
            
        elif vae_name == "taew2_2":
            model = Wan2_2_VAE_tiny(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device,
                need_scaled=False
            ).to(device)
            
        elif vae_name == "lighttaew2_1":
            model = WanVAE_tiny(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device,
                need_scaled=True
            ).to(device)
            
        elif vae_name == "lighttaew2_2":
            model = Wan2_2_VAE_tiny(
                vae_path=vae_path,
                dtype=torch_dtype,
                device=device,
                need_scaled=True
            ).to(device)
            
        else:
            raise ValueError(f"Unknown vae_name: {vae_name}")
        
        return ({
            "model": model,
            "vae_name": vae_name,
            "dtype": torch_dtype,
            "device": device,
        },)



class LightVAEDecode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae": ("VAE",),
                "latent": ("LATENT",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "decode"
    CATEGORY = "LightX2V"
    
    @torch.no_grad()
    def decode(self, vae: dict, latent: dict):
        model = vae["model"]
        dtype = vae["dtype"]
        device = vae["device"]

        latent_samples = latent["samples"].to(device, dtype)
        with torch.no_grad():
            video = model.decode(latent_samples.squeeze(0)).half().permute(0, 2, 3, 4, 1)

        if len(video.shape) == 5: #Combine batches
            video = video.reshape(-1, video.shape[-3], video.shape[-2], video.shape[-1])
        return (video.add_(1.0).div_(2.0),)


__all__ = [
    "VAEDecoderLoader",
    "LightVAEDecode"
]