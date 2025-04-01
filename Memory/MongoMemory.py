from langchain.chains import LLMChain



class MongoMemory:

    def __init__(self, collection):
        self.collection = collection

    def save_message(self, user_input, bot_response,subject):
        self.collection.insert_one({"user": user_input, "bot": bot_response,"subject":subject})

    def load_messages(self):
        messages = self.collection.find({}, {"_id": 0})
        return [f"User: {m['user']}\nBot: {m['bot']}" for m in messages]



#print(memory.chat_memory.messages)

#previous_messages = mongo_memory.load_messages()

#for msg in previous_messages:
    #parts = msg.split("\n")
    #memory.chat_memory.add_user_message(parts[0].replace("User: ", ""))
    #memory.chat_memory.add_ai_message(parts[1].replace("Bot: ", ""))

# Retrieve all messages
#chat_history = mongo_memory.load_messages()
#print("\n".join(chat_history))
