import re
import asyncio
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from .models import InsightRaw
from .ai_services import (
    transcribe_audio_real, 
    ocr_image_real, 
    analyze_sentiment_advanced,
    init_ai_services
)
import logging

logger = logging.getLogger(__name__)

# Initialize AI services
init_ai_services()


def anonymize_text(text: Optional[str]) -> Optional[str]:
    """Enhanced anonymization for GDPR compliance"""
    if not text:
        return text
    
    # Remove emails
    anon = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
    
    # Remove phone numbers (Italian formats)
    anon = re.sub(r'\b(?:\+39[-.\s]?)?\d{10,11}\b', '[PHONE_REDACTED]', anon)
    anon = re.sub(r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', '[PHONE_REDACTED]', anon)
    
    # Remove potential names (sequences of capitalized words)
    anon = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME_REDACTED]', anon)
    
    # Remove potential addresses (via/corso/viale patterns)
    anon = re.sub(r'\b(?:via|corso|viale|piazza)\s+[A-Za-z\s]+\d+', '[ADDRESS_REDACTED]', anon, flags=re.IGNORECASE)
    
    # Remove fiscal codes
    anon = re.sub(r'\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b', '[FISCAL_CODE_REDACTED]', anon)
    
    return anon


async def process_insight_async(session: Session, insight_id: str) -> None:
    """Async processing with real AI services"""
    ins = session.get(InsightRaw, insight_id)
    if not ins:
        logger.warning(f"Insight {insight_id} not found")
        return
    
    try:
        # Collect text sources
        text_sources = []
        if ins.text:
            text_sources.append(ins.text)
        
        # Process audio with real Whisper
        if ins.audio_url:
            logger.info(f"Transcribing audio for insight {insight_id}")
            transcription = await transcribe_audio_real(ins.audio_url)
            if transcription:
                text_sources.append(transcription)
        
        # Process image with real OCR
        ocr_text = None
        if ins.photo_url:
            logger.info(f"Processing OCR for insight {insight_id}")
            ocr_text = await ocr_image_real(ins.photo_url)
            if ocr_text:
                text_sources.append(ocr_text)
        
        # Merge all text sources
        merged_text = "\n".join([t for t in text_sources if t and t.strip()]) or None
        
        # Anonymize for privacy
        anon_text = anonymize_text(merged_text) if merged_text else None
        
        # Advanced sentiment analysis
        extracted = analyze_sentiment_advanced(anon_text) if anon_text else {"sentiment": "neutral"}
        
        # Update insight with processed data
        ins.text = anon_text
        ins.ocr_text = ocr_text or ins.ocr_text
        ins.extracted = extracted
        
        session.add(ins)
        session.commit()
        
        logger.info(f"Successfully processed insight {insight_id}")
        
    except Exception as e:
        logger.error(f"Failed to process insight {insight_id}: {e}")
        # Set error status in extracted field
        ins.extracted = {"sentiment": "neutral", "error": str(e)}
        session.add(ins)
        session.commit()


def process_insight(session: Session, insight_id: str) -> None:
    """Synchronous wrapper for async processing"""
    try:
        # Run async processing in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_insight_async(session, insight_id))
    except Exception as e:
        logger.error(f"Error in sync processing wrapper: {e}")
    finally:
        try:
            loop.close()
        except:
            pass


# Backward compatibility
def transcribe_audio_stub(audio_url: Optional[str]) -> Optional[str]:
    """Backward compatibility - now uses real AI"""
    if not audio_url:
        return None
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(transcribe_audio_real(audio_url))
        return result
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return f"[Errore trascrizione: {str(e)}]"
    finally:
        try:
            loop.close()
        except:
            pass


def ocr_image_stub(photo_url: Optional[str]) -> Optional[str]:
    """Backward compatibility - now uses real AI"""
    if not photo_url:
        return None
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(ocr_image_real(photo_url))
        return result
    except Exception as e:
        logger.error(f"OCR error: {e}")
        return f"[Errore OCR: {str(e)}]"
    finally:
        try:
            loop.close()
        except:
            pass


def basic_extraction(text: Optional[str]) -> Dict[str, Any]:
    """Enhanced extraction with real AI sentiment analysis"""
    return analyze_sentiment_advanced(text)