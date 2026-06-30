from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def convert_messages_to_langchain(mensagens_json):
    converted_messages = []
    for msg in mensagens_json:
        role = msg.get("role", "human").lower()
        content = msg.get("content", "")
        
        if role in ["user", "human"]:
            converted_messages.append(HumanMessage(content=content))
        elif role in ["assistant", "ai"]:
            converted_messages.append(AIMessage(content=content))
        elif role == "system":
            converted_messages.append(SystemMessage(content=content))
    return converted_messages