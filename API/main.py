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


client = MongoClient("mongodb://localhost:27017/")
db = client["chat_memory"]
collections = db["conversations"]

llm = ChatOllama(model="ChatAI")

template = """You are a great conversationalist.
Here is our conversation history on the subject of {subject}:
History:{history}
User: {input}
"""

prompt = PromptTemplate(input_variables=["history", "input", "subject"], template=template)
mongo_memory = MongoMemory(collections)

print(mongo_memory)

memory = ConversationBufferMemory(memory_key="history", input_key="input")

previous_messages = mongo_memory.load_messages()

for msg in previous_messages:
    parts = msg.split("\n")
    memory.chat_memory.add_user_message(parts[0].replace("User: ", ""))
    memory.chat_memory.add_ai_message(parts[1].replace("Bot: ", ""))

conversation = LLMChain(
    llm=ChatOllama(model="ChatAI"),
    memory=memory,
    verbose=True,
    prompt=prompt,
)

chat_history = mongo_memory.load_messages()


@app.post("/chat")
async def chat(message: ChatRequest):
    user_message = message.message
    subject = message.subject

    response = conversation.invoke({"input": user_message, "subject": subject})
    #response = conversation.predict(input=user_message, subject=subject)

    mongo_memory.save_message(user_message, response, subject)
    #mongo_memory.save_message({ "user_input": user_message,"bot_response": response,"subject": subject})

    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
