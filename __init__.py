from .nodes import (
    VAEDecoderLoader,
    LightVAEDecode
)

NODE_CLASS_MAPPINGS = {
    "Lightx2v-VAEDecoderLoader": VAEDecoderLoader,
    "Lightx2v-VAEDecode": LightVAEDecode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Lightx2v-VAEDecoderLoader": "LightX2V VAE Decoder Loader",
    "Lightx2v-VAEDecode": "LightX2V VAE Decode",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
