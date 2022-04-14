from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from text_generator import get_generated_text

app = FastAPI()

class Info(BaseModel):
    prefix: str
    model_type: bool = False

@app.post("/generate")
async def generate(info: Info):
    return get_generated_text(info.prefix, info.model_type)