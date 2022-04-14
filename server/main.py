from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from text_generator import get_generated_text

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Info(BaseModel):
    prefix: str
    model_type: bool = False

@app.post("/generate")
async def generate(info: Info):
    return { "result" : get_generated_text(info.prefix, info.model_type) }