from langchain_core.messages import BaseMessage

class ChatPort:
    def __init__(self, llm_client_adapter):
        self.chat = llm_client_adapter


    def generate_response(self, messages: list) -> BaseMessage:
        return self.chat.invoke(messages)