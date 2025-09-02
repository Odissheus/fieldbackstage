#!/usr/bin/env python3
"""
Test script for AI/ML features in React Field Insights
Tests OCR, Audio Transcription, Sentiment Analysis, and Q&A
"""

import os
import sys
import asyncio
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent / "server"))

from server.ai_services import (
    transcribe_audio_real,
    ocr_image_real,
    analyze_sentiment_advanced,
    qa_with_rag,
    init_ai_services
)
from server.config import settings

def check_ai_configuration():
    """Check AI configuration and requirements"""
    print("🔧 AI Configuration Check")
    print("=" * 50)
    
    # Show configured API key (masked for security)
    api_key_status = "✅ CONFIGURED" if settings.OPENAI_API_KEY else "❌ MISSING"
    if settings.OPENAI_API_KEY:
        masked_key = f"{settings.OPENAI_API_KEY[:8]}...{settings.OPENAI_API_KEY[-8:]}"
    else:
        masked_key = "Not set"
    
    config_status = {
        "OpenAI API Key": f"{api_key_status} ({masked_key})",
        "AI Processing Enabled": settings.ENABLE_AI_PROCESSING,
        "OpenAI Model": settings.OPENAI_MODEL,
        "Whisper Model": settings.OPENAI_WHISPER_MODEL,
        "ChromaDB Path": settings.CHROMADB_PATH,
        "Tesseract Path": settings.TESSERACT_CMD or "Auto-detect"
    }
    
    all_good = True
    for key, value in config_status.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}: {value}")
        if not value and key in ["OpenAI API Key", "AI Processing Enabled"]:
            all_good = False
    
    print()
    return all_good

async def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("🧠 Testing Sentiment Analysis")
    print("-" * 30)
    
    test_texts = [
        "Il prodotto funziona benissimo, i clienti sono molto soddisfatti!",
        "Abbiamo grossi problemi con gli effetti collaterali del farmaco",
        "La situazione è normale, nessuna novità particolare da segnalare"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text[:50]}...")
        result = analyze_sentiment_advanced(text)
        print(f"   Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"   Confidence: {result.get('confidence', 0):.2f}")
        print(f"   Polarity: {result.get('polarity_score', 0):.2f}")

async def test_audio_transcription():
    """Test audio transcription"""
    print("\n🎤 Testing Audio Transcription")
    print("-" * 30)
    
    # Test with a sample audio URL (you would need a real audio file)
    test_url = input("Enter an audio file URL to test (or press Enter to skip): ").strip()
    
    if test_url:
        print(f"Transcribing: {test_url}")
        try:
            result = await transcribe_audio_real(test_url)
            print(f"Transcription: {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Audio transcription test skipped")

async def test_ocr():
    """Test OCR processing"""
    print("\n📷 Testing OCR")
    print("-" * 30)
    
    # Test with a sample image URL
    test_url = input("Enter an image URL to test OCR (or press Enter to skip): ").strip()
    
    if test_url:
        print(f"Processing OCR for: {test_url}")
        try:
            result = await ocr_image_real(test_url)
            print(f"OCR Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("OCR test skipped")

async def test_qa_rag():
    """Test Q&A with RAG"""
    print("\n🤔 Testing Q&A with RAG")
    print("-" * 30)
    
    test_queries = [
        "Quali sono i trend di dosaggio?",
        "Problemi con effetti collaterali",
        "Feedback sui prezzi"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = await qa_with_rag(query)
            print(f"Answer: {result.get('answer', 'No answer')[:100]}...")
            print(f"Citations: {len(result.get('citations', []))}")
        except Exception as e:
            print(f"Error: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking Dependencies")
    print("-" * 30)
    
    dependencies = [
        ("openai", "OpenAI API client"),
        ("PIL", "Pillow for image processing"),
        ("pytesseract", "Tesseract OCR"),
        ("textblob", "TextBlob for sentiment"),
        ("langchain", "LangChain framework"),
        ("chromadb", "ChromaDB vector database")
    ]
    
    missing = []
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - MISSING")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r server/requirements.txt")
        return False
    
    return True

def system_requirements_info():
    """Show system requirements for AI features"""
    print("\n📋 System Requirements for AI Features")
    print("=" * 50)
    print("""
🔑 Required Environment Variables:
   - OPENAI_API_KEY: Your OpenAI API key
   - ENABLE_AI_PROCESSING=true: Enable AI features
   
🐙 Optional Configuration:
   - OPENAI_MODEL: GPT model (default: gpt-4o-mini)
   - OPENAI_WHISPER_MODEL: Whisper model (default: whisper-1)
   - TESSERACT_CMD: Path to tesseract executable
   - CHROMADB_PATH: Path for vector database (default: ./data/chromadb)

🖥️  System Dependencies:
   - Tesseract OCR (for image text extraction)
     • Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-ita
     • macOS: brew install tesseract tesseract-lang
     • Windows: Download from GitHub releases
   
💰 OpenAI API Costs (approximate):
   - Whisper: $0.006 per minute of audio
   - GPT-4o-mini: $0.00015 per 1K input tokens
   - Text embeddings: $0.00002 per 1K tokens
   
🚀 Features Enabled:
   ✅ Audio → Text transcription (Whisper)
   ✅ Image → Text extraction (Tesseract + GPT)
   ✅ Advanced sentiment analysis (TextBlob + GPT)
   ✅ Smart Q&A with RAG (ChromaDB + GPT)
   ✅ GDPR-compliant data anonymization
""")

async def main():
    """Main test function"""
    print("🤖 React Field Insights AI/ML Test Suite")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Missing dependencies. Please install requirements first.")
        return
    
    # Check configuration
    config_ok = check_ai_configuration()
    
    if not config_ok:
        print("\n⚠️  AI features not fully configured")
        system_requirements_info()
        
        proceed = input("\nContinue with limited testing? (y/n): ").lower()
        if proceed != 'y':
            return
    
    # Initialize AI services
    print("\n🔄 Initializing AI services...")
    try:
        init_ai_services()
        print("✅ AI services initialized")
    except Exception as e:
        print(f"❌ Failed to initialize AI services: {e}")
    
    # Run tests
    await test_sentiment_analysis()
    await test_audio_transcription()
    await test_ocr()
    await test_qa_rag()
    
    print("\n✅ AI Testing Complete!")
    system_requirements_info()

if __name__ == "__main__":
    asyncio.run(main())

