from fastapi import FastAPI
from urllib import request
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import ollama
from langchain.prompts import PromptTemplate

app = FastAPI()

class Request(BaseModel):
    input: str

@app.post("/chat")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)