# config.py
import os

NIM_API_KEY = os.environ["NIM_API_KEY"]
NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Good general-purpose NIM models to start with
LLM_MODEL = "meta/llama-3.1-70b-instruct"
EMBED_MODEL = "nvidia/nv-embedqa-e5-v5"