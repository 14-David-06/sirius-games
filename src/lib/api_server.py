"""
Servidor FastAPI para el Agente RAG Realtime
Conecta el agente Python con la interfaz Next.js
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json
import os
from datetime import datetime

# Importar nuestro agente RAG
from realtime_rag_agent import RealtimeRAGAgent

app = FastAPI(title="ALMA RAG API", version="1.0.0")

# Configurar CORS para Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    api_key: Optional[str] = None

class DocumentRequest(BaseModel):
    documents: List[Dict]
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

# Instancia global del agente (en producción usar un patrón mejor)
_agent_instance = None

def get_agent(api_key: str = None) -> RealtimeRAGAgent:
    """Obtener instancia del agente RAG"""
    global _agent_instance
    
    if _agent_instance is None:
        # Usar API key del request o variable de entorno
        openai_key = api_key or os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise HTTPException(
                status_code=400, 
                detail="OpenAI API key required"
            )
        
        _agent_instance = RealtimeRAGAgent(openai_api_key=openai_key)
    
    return _agent_instance

@app.get("/")
async def root():
    """Endpoint de salud"""
    return {
        "message": "ALMA RAG API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat normal (no streaming)"""
    try:
        agent = get_agent(request.api_key)
        
        # Obtener respuesta completa
        full_response = ""
        async for chunk in agent.chat_stream(request.message, request.session_id):
            full_response += chunk
        
        return ChatResponse(
            response=full_response,
            session_id=request.session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Chat con streaming en tiempo real"""
    
    async def generate_stream():
        try:
            agent = get_agent(request.api_key)
            
            # Enviar evento de inicio
            yield f"data: {json.dumps({'type': 'start', 'session_id': request.session_id})}\n\n"
            
            # Stream de chunks de respuesta
            async for chunk in agent.chat_stream(request.message, request.session_id):
                if chunk:  # Solo enviar chunks no vacíos
                    event_data = {
                        'type': 'stream',
                        'chunk': chunk,
                        'session_id': request.session_id
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
            
            # Enviar evento de finalización
            yield f"data: {json.dumps({'type': 'complete', 'session_id': request.session_id})}\n\n"
            
        except Exception as e:
            # Enviar evento de error
            error_data = {
                'type': 'error',
                'error': str(e),
                'session_id': request.session_id
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

@app.post("/documents/add")
async def add_documents(request: DocumentRequest):
    """Agregar documentos a la base de conocimientos"""
    try:
        agent = get_agent(request.api_key)
        
        # Validar documentos
        if not request.documents:
            raise HTTPException(status_code=400, detail="No documents provided")
        
        # Agregar documentos al vectorstore
        agent.add_documents(request.documents)
        
        return {
            "message": f"Successfully added {len(request.documents)} documents",
            "count": len(request.documents),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/search")
async def search_documents(
    query: str,
    limit: int = 5,
    category: Optional[str] = None,
    api_key: Optional[str] = None
):
    """Buscar documentos en la base de conocimientos"""
    try:
        agent = get_agent(api_key)
        
        # Configurar filtros
        filter_dict = {}
        if category:
            filter_dict["category"] = category
        
        # Buscar documentos
        docs = agent.vectorstore.similarity_search(
            query,
            k=limit,
            filter=filter_dict if filter_dict else None
        )
        
        # Formatear resultados
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": getattr(doc, 'relevance_score', None)
            })
        
        return {
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/{session_id}/memory")
async def get_session_memory(session_id: str, api_key: Optional[str] = None):
    """Obtener memoria de una sesión específica"""
    try:
        agent = get_agent(api_key)
        
        # En una implementación real, obtendrías esto del checkpointer
        # Por ahora devolvemos información básica
        return {
            "session_id": session_id,
            "message": "Memory retrieval not implemented yet",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str, api_key: Optional[str] = None):
    """Limpiar memoria de una sesión"""
    try:
        # En una implementación real, limpiarías la memoria de la sesión
        return {
            "message": f"Session {session_id} cleared",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Verificación de salud del servicio"""
    try:
        # Verificar que el agente puede inicializarse
        agent = get_agent()
        
        return {
            "status": "healthy",
            "agent_initialized": agent is not None,
            "vectorstore_ready": agent.vectorstore is not None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Punto de entrada para desarrollo
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando servidor ALMA RAG API...")
    print("📍 URL: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )