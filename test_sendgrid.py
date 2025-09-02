#!/usr/bin/env python3
"""
Script di test per verificare la configurazione SendGrid
Esegui questo script per testare l'invio di email con SendGrid
"""

import os
import sys
from pathlib import Path

# Aggiungi la directory server al path per importare i moduli
sys.path.insert(0, str(Path(__file__).parent / "server"))

from server.email import send_mail
from server.config import settings

def test_sendgrid_config():
    """Testa la configurazione SendGrid"""
    print("🔧 Testing SendGrid Configuration...")
    print(f"SMTP_HOST: {settings.SMTP_HOST}")
    print(f"SMTP_PORT: {settings.SMTP_PORT}")
    print(f"SMTP_USER: {settings.SMTP_USER}")
    print(f"SMTP_FROM: {settings.SMTP_FROM}")
    print(f"SMTP_PASS: {'*' * 20 if settings.SMTP_PASS else 'NOT SET'}")
    print()
    
    # Verifica che tutte le configurazioni siano presenti
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASS, settings.SMTP_FROM]):
        print("❌ Configurazione incompleta!")
        print("Assicurati di aver impostato tutte le variabili d'ambiente:")
        print("- SMTP_HOST")
        print("- SMTP_USER") 
        print("- SMTP_PASS")
        print("- SMTP_FROM")
        return False
    
    print("✅ Configurazione completa!")
    return True

def send_test_email(to_email: str = None):
    """Invia una email di test"""
    if not to_email:
        to_email = input("Inserisci l'email di destinazione per il test: ").strip()
    
    if not to_email:
        print("❌ Email di destinazione richiesta")
        return False
    
    print(f"📧 Invio email di test a: {to_email}")
    
    try:
        error = send_mail(
            to_address=to_email,
            subject="Test SendGrid - React Field Insights",
            body_text="""Ciao!

Questa è una email di test per verificare la configurazione SendGrid del progetto React Field Insights.

Se ricevi questa email, la configurazione SendGrid è funzionante correttamente!

Dettagli configurazione:
- SMTP Host: smtp.sendgrid.net
- SMTP Port: 587
- From: danielepili@react-company.com

Saluti,
Il team React Field Insights
"""
        )
        
        if error:
            print(f"❌ Errore nell'invio: {error}")
            return False
        else:
            print("✅ Email inviata con successo!")
            print(f"Controlla la casella di posta di {to_email}")
            return True
            
    except Exception as e:
        print(f"❌ Eccezione durante l'invio: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 SendGrid Test Tool")
    print("=" * 50)
    
    # Test configurazione
    if not test_sendgrid_config():
        print("\n💡 Per configurare SendGrid, aggiungi queste variabili d'ambiente:")
        print("export SMTP_HOST=smtp.sendgrid.net")
        print("export SMTP_PORT=587")
        print("export SMTP_USER=apikey")
        print("export SMTP_PASS=your-sendgrid-api-key-here")
        print("export SMTP_FROM=danielepili@react-company.com")
        sys.exit(1)
    
    print()
    
    # Test invio email
    if len(sys.argv) > 1:
        # Email passata come argomento
        email = sys.argv[1]
        send_test_email(email)
    else:
        # Chiedi interattivamente
        send_test_email()
