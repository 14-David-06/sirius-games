"""
Agente Realtime RAG para Sirius Games
Implementación práctica usando LangGraph
"""

import asyncio
from typing import Dict, List, AsyncIterator
from dataclasses import dataclass
from datetime import datetime

# LangGraph imports
from langgraph import Graph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolExecutor

# LangChain imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter

@dataclass
class AgentState:
    """Estado del agente realtime"""
    user_input: str
    context: str = ""
    response: str = ""
    memory: List[Dict] = None
    retrieved_docs: List = None
    session_id: str = ""
    timestamp: datetime = None

class RealtimeRAGAgent:
    """Agente RAG en tiempo real para ALMA"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            streaming=True,
            api_key=openai_api_key
        )
        
        self.embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        self.vectorstore = None
        self.memory = MemorySaver()
        self.graph = None
        
        # Inicializar componentes
        self._setup_vectorstore()
        self._create_graph()
    
    def _setup_vectorstore(self):
        """Configurar vectorstore para RAG"""
        try:
            # Intentar cargar vectorstore existente
            self.vectorstore = Chroma(
                persist_directory="./knowledge_base",
                embedding_function=self.embeddings
            )
            print("✅ Vectorstore cargado exitosamente")
        except Exception as e:
            print(f"⚠️ Creando nuevo vectorstore: {e}")
            self._create_initial_vectorstore()
    
    def _create_initial_vectorstore(self):
        """Crear vectorstore inicial con documentos de ejemplo"""
        # Documentos de ejemplo sobre Sirius Games
        sample_docs = [
            {
                "content": "Sirius Games es un proyecto de desarrollo de videojuegos que utiliza Next.js, TypeScript y React para crear experiencias interactivas.",
                "metadata": {"source": "project_info", "category": "general"}
            },
            {
                "content": "ALMA es un asistente de inteligencia artificial integrado en Sirius Games que puede ayudar con consultas sobre desarrollo, gaming y tecnología.",
                "metadata": {"source": "alma_info", "category": "ai"}
            },
            {
                "content": "El proyecto utiliza Tailwind CSS para el diseño y tiene una arquitectura moderna basada en componentes reutilizables.",
                "metadata": {"source": "tech_stack", "category": "technical"}
            }
        ]
        
        # Crear vectorstore
        texts = [doc["content"] for doc in sample_docs]
        metadatas = [doc["metadata"] for doc in sample_docs]
        
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=self.embeddings,
            persist_directory="./knowledge_base"
        )
    
    def _create_graph(self):
        """Crear el grafo del agente"""
        workflow = Graph()
        
        # Definir nodos
        workflow.add_node("retrieve", self._retrieve_context)
        workflow.add_node("generate", self._generate_response)
        workflow.add_node("update_memory", self._update_memory)
        
        # Definir flujo
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", "update_memory")
        workflow.add_edge("update_memory", "__end__")
        
        # Punto de entrada
        workflow.set_entry_point("retrieve")
        
        # Compilar con memoria
        self.graph = workflow.compile(checkpointer=self.memory)
    
    async def _retrieve_context(self, state: AgentState) -> Dict:
        """Recuperar contexto relevante del vectorstore"""
        try:
            # Búsqueda semántica
            docs = self.vectorstore.similarity_search(
                state.user_input,
                k=3,  # Top 3 documentos más relevantes
                filter=None  # Sin filtros por ahora
            )
            
            # Formatear contexto
            context = "\n".join([
                f"Fuente: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
                for doc in docs
            ])
            
            print(f"🔍 Contexto recuperado: {len(docs)} documentos")
            
            return {
                "context": context,
                "retrieved_docs": docs,
                "user_input": state.user_input
            }
            
        except Exception as e:
            print(f"❌ Error en retrieval: {e}")
            return {
                "context": "No se pudo recuperar contexto específico.",
                "retrieved_docs": [],
                "user_input": state.user_input
            }
    
    async def _generate_response(self, state: Dict) -> AsyncIterator[Dict]:
        """Generar respuesta streaming con RAG"""
        context = state.get("context", "")
        user_input = state.get("user_input", "")
        
        # Obtener memoria de conversaciones anteriores
        memory_context = self._format_memory_context(state.get("memory", []))
        
        # Construir prompt con RAG
        system_prompt = f"""Eres ALMA, un asistente de IA para Sirius Games.

Contexto de conversaciones anteriores:
{memory_context}

Información relevante de la base de conocimientos:
{context}

Instrucciones:
- Responde de manera útil y precisa
- Usa la información del contexto cuando sea relevante
- Si no tienes información específica, sé honesto al respecto
- Mantén un tono amigable y profesional
- Enfócate en ayudar con temas relacionados con Sirius Games, desarrollo y gaming

Pregunta del usuario: {user_input}"""

        try:
            # Stream de respuesta
            response_chunks = []
            
            async for chunk in self.llm.astream(system_prompt):
                chunk_content = chunk.content
                response_chunks.append(chunk_content)
                
                # Yield cada chunk para streaming
                yield {
                    "chunk": chunk_content,
                    "type": "stream"
                }
            
            # Respuesta completa
            full_response = "".join(response_chunks)
            
            yield {
                "response": full_response,
                "user_input": user_input,
                "context": context,
                "type": "complete"
            }
            
        except Exception as e:
            error_response = f"Lo siento, ocurrió un error al generar la respuesta: {str(e)}"
            yield {
                "response": error_response,
                "user_input": user_input,
                "context": context,
                "type": "error"
            }
    
    def _format_memory_context(self, memory: List[Dict]) -> str:
        """Formatear contexto de memoria"""
        if not memory:
            return "No hay conversaciones anteriores."
        
        # Tomar las últimas 3 interacciones
        recent_memory = memory[-3:] if len(memory) > 3 else memory
        
        formatted = []
        for turn in recent_memory:
            formatted.append(f"Usuario: {turn.get('user', '')}")
            formatted.append(f"ALMA: {turn.get('assistant', '')}")
        
        return "\n".join(formatted)
    
    async def _update_memory(self, state: Dict) -> Dict:
        """Actualizar memoria de la conversación"""
        memory = state.get("memory", [])
        
        # Agregar nueva interacción
        new_turn = {
            "user": state.get("user_input", ""),
            "assistant": state.get("response", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        memory.append(new_turn)
        
        # Mantener solo las últimas 10 interacciones
        if len(memory) > 10:
            memory = memory[-10:]
        
        return {
            "memory": memory,
            "final_response": state.get("response", "")
        }
    
    async def chat_stream(self, user_input: str, session_id: str = "default") -> AsyncIterator[str]:
        """Interfaz principal para chat streaming"""
        
        # Configuración de thread para persistencia
        config = {"configurable": {"thread_id": session_id}}
        
        # Input inicial
        initial_state = {
            "user_input": user_input,
            "session_id": session_id,
            "timestamp": datetime.now()
        }
        
        try:
            # Ejecutar el grafo
            async for chunk in self.graph.astream(initial_state, config=config):
                # Procesar chunks del generador
                if "generate" in chunk:
                    generate_data = chunk["generate"]
                    if isinstance(generate_data, dict):
                        if generate_data.get("type") == "stream":
                            yield generate_data.get("chunk", "")
                        elif generate_data.get("type") == "complete":
                            # Finalización de la respuesta
                            break
                            
        except Exception as e:
            yield f"\n\n❌ Error: {str(e)}"
    
    def add_documents(self, documents: List[Dict]):
        """Agregar nuevos documentos al vectorstore"""
        texts = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
        self.vectorstore.persist()
        
        print(f"✅ {len(documents)} documentos agregados al vectorstore")

# Herramientas adicionales para el agente
@tool
def search_knowledge_base(query: str, category: str = "all") -> str:
    """Buscar en la base de conocimientos por categoría"""
    # Esta función sería llamada por el agente cuando necesite búsquedas específicas
    return f"Resultados de búsqueda para: {query} en categoría: {category}"

@tool  
def get_system_info() -> str:
    """Obtener información del sistema Sirius Games"""
    return """
    Sirius Games - Sistema de información:
    - Framework: Next.js 16 con TypeScript
    - Styling: Tailwind CSS
    - AI Agent: ALMA (Asistente integrado)
    - Arquitectura: Componentes modulares
    - Estado: Activo y funcionando
    """

# Ejemplo de uso
if __name__ == "__main__":
    async def main():
        # Inicializar agente (necesitas tu API key de OpenAI)
        agent = RealtimeRAGAgent(openai_api_key="tu-api-key-aqui")
        
        # Simular chat
        user_query = "¿Qué es ALMA y cómo funciona?"
        
        print("🤖 ALMA: ", end="", flush=True)
        
        async for chunk in agent.chat_stream(user_query, session_id="test_session"):
            print(chunk, end="", flush=True)
        
        print("\n")
    
    # Ejecutar ejemplo
    # asyncio.run(main())