from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langfuse.langchain import CallbackHandler
from src.rag.build_graph import build_rag_graph
from src.api.schemas.chat_schema import ChatRequest
from src.services.messages_converter import convert_messages_to_langchain


app = FastAPI(title="API Multi-Agentes RAG")
app_graph = build_rag_graph()


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        langfuse_handler = CallbackHandler()
        list_messages = convert_messages_to_langchain(request.messages)

        estado_inicial = {
            "messages": list_messages,
            "possibles_pdfs_titles": request.possibles_pdfs_titles
        }

        resultado = app_graph.invoke(
            estado_inicial,
            config={
                "callbacks": [langfuse_handler],
                "metadata": {"langfuse_session_id": request.session_id}
            }
        )

        ai_response = resultado["messages"][-1].content
        return {
            "answer": ai_respose if ai_respose else "Sorry, I could not process a response for this..."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))