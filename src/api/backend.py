from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langfuse.langchain import CallbackHandler
from src.rag.build_graph import build_rag_graph
from src.api.schemas.chat_schema import ChatRequest
from src.services.opensearch import OpenSearchClient
from src.services.messages_converter import convert_messages_to_langchain


app = FastAPI(title="API Multi-Agentes RAG")
app_graph = build_rag_graph()
client = OpenSearchClient()
langfuse_handler = CallbackHandler()


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
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
            "answer": ai_response if ai_respose else "Sorry, I could not process a response for this..."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/books")
def list_books_endpoint():
    try:
        books = client.list_books(index_name="metadata-pdfs")
        return {"books": books}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))