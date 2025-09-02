"""
AI/ML Services for React Field Insights
Handles OCR, Audio Transcription, Sentiment Analysis, and LLM Q&A
"""

import os
import tempfile
import httpx
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

from openai import OpenAI
from PIL import Image
import pytesseract
from textblob import TextBlob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document
import chromadb
from chromadb.config import Settings as ChromaSettings

from .config import settings

logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = None
if settings.OPENAI_API_KEY:
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Initialize ChromaDB for Q&A RAG
chroma_client = None
collection = None
embeddings = None

def init_ai_services():
    """Initialize AI services and ChromaDB"""
    global chroma_client, collection, embeddings
    
    if not settings.ENABLE_AI_PROCESSING:
        logger.info("AI processing disabled")
        return
    
    if not settings.OPENAI_API_KEY:
        logger.warning("OpenAI API key not configured - AI features will be limited")
        return
    
    try:
        # Initialize ChromaDB
        os.makedirs(settings.CHROMADB_PATH, exist_ok=True)
        chroma_client = chromadb.PersistentClient(
            path=settings.CHROMADB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection for reports
        collection = chroma_client.get_or_create_collection(
            name="field_insights_reports",
            metadata={"description": "Field insights reports and summaries"}
        )
        
        # Initialize embeddings
        embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        
        logger.info("AI services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize AI services: {e}")


async def transcribe_audio_real(audio_url: Optional[str]) -> Optional[str]:
    """
    Real audio transcription using OpenAI Whisper API
    """
    if not audio_url or not openai_client:
        return None
    
    if not settings.ENABLE_AI_PROCESSING:
        return "[Audio transcription disabled]"
    
    try:
        # Download audio file
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(audio_url)
            response.raise_for_status()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Transcribe with Whisper
            with open(temp_path, "rb") as audio_file:
                transcript = openai_client.audio.transcriptions.create(
                    model=settings.OPENAI_WHISPER_MODEL,
                    file=audio_file,
                    language="it"  # Italian for pharmaceutical context
                )
            
            logger.info(f"Successfully transcribed audio: {len(transcript.text)} characters")
            return transcript.text
            
        finally:
            # Cleanup temp file
            os.unlink(temp_path)
            
    except Exception as e:
        logger.error(f"Audio transcription failed: {e}")
        return f"[Errore trascrizione: {str(e)}]"


async def ocr_image_real(photo_url: Optional[str]) -> Optional[str]:
    """
    Real OCR using Tesseract + OpenAI GPT for enhancement
    """
    if not photo_url:
        return None
    
    if not settings.ENABLE_AI_PROCESSING:
        return "[OCR processing disabled]"
    
    try:
        # Download image
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(photo_url)
            response.raise_for_status()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Open and process image
            image = Image.open(temp_path)
            
            # Basic OCR with Tesseract
            if settings.TESSERACT_CMD:
                pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
            
            # Extract text with Italian language support
            ocr_text = pytesseract.image_to_string(
                image, 
                lang='ita+eng',
                config='--psm 6'
            ).strip()
            
            # Enhance with OpenAI if available and text found
            if ocr_text and openai_client and len(ocr_text) > 10:
                enhanced_text = await enhance_ocr_with_ai(ocr_text)
                return enhanced_text or ocr_text
            
            logger.info(f"OCR extracted: {len(ocr_text)} characters")
            return ocr_text if ocr_text else None
            
        finally:
            # Cleanup temp file
            os.unlink(temp_path)
            
    except Exception as e:
        logger.error(f"OCR processing failed: {e}")
        return f"[Errore OCR: {str(e)}]"


async def enhance_ocr_with_ai(raw_ocr: str) -> Optional[str]:
    """
    Enhance OCR text using OpenAI to fix errors and improve readability
    """
    if not openai_client:
        return raw_ocr
    
    try:
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Sei un assistente specializzato nel correggere testo estratto tramite OCR. "
                              "Il testo riguarda il settore farmaceutico e vendite. "
                              "Correggi errori di riconoscimento mantenendo il significato originale. "
                              "Rispondi solo con il testo corretto, senza spiegazioni."
                },
                {
                    "role": "user",
                    "content": f"Correggi questo testo OCR:\n\n{raw_ocr}"
                }
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        enhanced = response.choices[0].message.content.strip()
        logger.info("OCR text enhanced with AI")
        return enhanced
        
    except Exception as e:
        logger.error(f"OCR enhancement failed: {e}")
        return raw_ocr


def analyze_sentiment_advanced(text: Optional[str]) -> Dict[str, Any]:
    """
    Advanced sentiment analysis using TextBlob + OpenAI
    """
    if not text:
        return {"sentiment": "neutral", "confidence": 0.0, "emotions": {}}
    
    try:
        # Basic sentiment with TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Map polarity to categories
        if polarity > 0.1:
            basic_sentiment = "positive"
        elif polarity < -0.1:
            basic_sentiment = "negative"
        else:
            basic_sentiment = "neutral"
        
        result = {
            "sentiment": basic_sentiment,
            "confidence": abs(polarity),
            "subjectivity": subjectivity,
            "polarity_score": polarity
        }
        
        # Enhanced analysis with OpenAI if available
        if openai_client and settings.ENABLE_AI_PROCESSING:
            enhanced = analyze_sentiment_with_ai(text)
            if enhanced:
                result.update(enhanced)
        
        return result
        
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return {"sentiment": "neutral", "confidence": 0.0, "error": str(e)}


def analyze_sentiment_with_ai(text: str) -> Optional[Dict[str, Any]]:
    """
    Enhanced sentiment analysis using OpenAI for pharmaceutical/sales context
    """
    try:
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Analizza il sentiment di questo testo dal settore farmaceutico/vendite. "
                              "Rispondi in formato JSON con: sentiment (positive/negative/neutral), "
                              "confidence (0-1), key_topics (array), emotions (object con fear, trust, satisfaction, concern). "
                              "Considera il contesto medico/commerciale."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            max_tokens=200,
            temperature=0.1
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        logger.info("Enhanced sentiment analysis completed")
        return result
        
    except Exception as e:
        logger.error(f"AI sentiment analysis failed: {e}")
        return None


async def qa_with_rag(query: str, product_line_id: Optional[str] = None, 
                     tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Advanced Q&A using RAG (Retrieval Augmented Generation) with ChromaDB + OpenAI
    """
    if not openai_client or not collection:
        return {
            "answer": "Sistema Q&A non configurato",
            "citations": [],
            "error": "OpenAI or ChromaDB not initialized"
        }
    
    try:
        # Create query embedding
        query_embedding = embeddings.embed_query(query)
        
        # Search similar documents in ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={
                "$and": [
                    {"tenant_id": {"$eq": tenant_id}} if tenant_id else {},
                    {"product_line_id": {"$eq": product_line_id}} if product_line_id else {}
                ]
            } if tenant_id or product_line_id else None
        )
        
        # Build context from retrieved documents
        context_docs = []
        citations = []
        
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                context_docs.append(doc)
                citations.append({
                    "reportId": metadata.get("report_id"),
                    "section": metadata.get("section", "summary"),
                    "weekId": metadata.get("week_id"),
                    "score": results['distances'][0][i] if results['distances'] else 0.0
                })
        
        context = "\n\n".join(context_docs[:3])  # Use top 3 results
        
        # Generate answer with OpenAI
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Sei un assistente esperto del settore farmaceutico che risponde a domande "
                              "basandoti sui report di campo forniti. Rispondi in italiano, sii preciso e "
                              "cita i dati specifici quando possibile. Se i dati non sono sufficienti, "
                              "dillo chiaramente."
                },
                {
                    "role": "user",
                    "content": f"Contesto dai report:\n{context}\n\nDomanda: {query}"
                }
            ],
            max_tokens=500,
            temperature=0.2
        )
        
        answer = response.choices[0].message.content
        
        logger.info(f"Q&A completed for query: {query[:50]}...")
        
        return {
            "answer": answer,
            "citations": citations[:3],
            "context_used": len(context_docs)
        }
        
    except Exception as e:
        logger.error(f"Q&A with RAG failed: {e}")
        return {
            "answer": f"Errore nel sistema Q&A: {str(e)}",
            "citations": [],
            "error": str(e)
        }


def index_report_for_rag(report_id: str, executive_summary: str, ci_summary: str,
                        week_id: str, tenant_id: str, product_line_id: str):
    """
    Index a report in ChromaDB for RAG Q&A
    """
    if not collection or not embeddings:
        return
    
    try:
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        documents = []
        metadatas = []
        ids = []
        
        # Index executive summary
        if executive_summary:
            summary_chunks = text_splitter.split_text(executive_summary)
            for i, chunk in enumerate(summary_chunks):
                documents.append(chunk)
                metadatas.append({
                    "report_id": report_id,
                    "section": "executive_summary",
                    "week_id": week_id,
                    "tenant_id": tenant_id,
                    "product_line_id": product_line_id,
                    "chunk_index": i
                })
                ids.append(f"{report_id}_summary_{i}")
        
        # Index CI summary
        if ci_summary:
            ci_chunks = text_splitter.split_text(ci_summary)
            for i, chunk in enumerate(ci_chunks):
                documents.append(chunk)
                metadatas.append({
                    "report_id": report_id,
                    "section": "ci_summary",
                    "week_id": week_id,
                    "tenant_id": tenant_id,
                    "product_line_id": product_line_id,
                    "chunk_index": i
                })
                ids.append(f"{report_id}_ci_{i}")
        
        if documents:
            # Generate embeddings and store
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Indexed report {report_id} with {len(documents)} chunks")
        
    except Exception as e:
        logger.error(f"Failed to index report {report_id}: {e}")


# Compatibility functions for existing code
async def transcribe_audio_stub(audio_url: Optional[str]) -> Optional[str]:
    """Backward compatibility wrapper"""
    return await transcribe_audio_real(audio_url)


async def ocr_image_stub(photo_url: Optional[str]) -> Optional[str]:
    """Backward compatibility wrapper"""
    return await ocr_image_real(photo_url)


def basic_extraction(text: Optional[str]) -> Dict[str, Any]:
    """Enhanced extraction with real AI"""
    return analyze_sentiment_advanced(text)

