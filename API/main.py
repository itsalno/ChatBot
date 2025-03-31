from fastapi import FastAPI
from urllib import request
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import ollama
from langchain.prompts import PromptTemplate

from Memory.MongoMemory import MongoMemory

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    subject: str

client=MongoClient("mongodb://localhost:27017/")
db=client["chat_memory"]
collections=db["conversations"]


llm=ChatOllama(model="ChatAI")

template = """You are a great conversationalist.
Here is our conversation history on the subject of {subject}:
{history}
User: {input}
Assistant:"""

prompt = PromptTemplate(input_variables=["history", "input","subject"], template=template)
mongo_memory = MongoMemory(collections)

memory = mongo_memory

conversation = LLMChain(
        llm=ChatOllama(model="ChatAI"),
        memory=memory,
        verbose=True,
    )

chat_history = mongo_memory.load_messages()
@app.post("/chat")
async def chat(message: ChatRequest):
    user_message = message.message
    subject = message.subject

    response = conversation.predict(input=user_message, subject=subject)

    mongo_memory.save_message({ "user": user_message,"bot_response": response,"subject": subject})

    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)