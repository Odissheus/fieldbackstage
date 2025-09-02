# Setup SendGrid per React Field Insights

## Configurazione Completata ✅

Le seguenti modifiche sono state applicate al progetto per integrare SendGrid:

### 1. Modifiche al Codice

- **`server/config.py`**: Aggiunta configurazione `SMTP_FROM`
- **`server/email.py`**: Aggiornata per utilizzare `SMTP_FROM` come mittente

### 2. Configurazione Variabili d'Ambiente

Aggiungi queste variabili d'ambiente al tuo sistema o file `.env`:

```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=YOUR_SENDGRID_API_KEY
SMTP_FROM=danielepili@react-company.com
```

## Come Utilizzare

### Per Sviluppo Locale

1. Crea un file `.env` nella root del progetto
2. Copia le variabili d'ambiente sopra nel file `.env`
3. Riavvia il server FastAPI

### Per Produzione

1. Configura le variabili d'ambiente nel tuo sistema di deployment
2. Assicurati che tutte le variabili SMTP siano impostate

## Test della Configurazione

Utilizza lo script di test fornito:

```bash
# Test interattivo
python test_sendgrid.py

# Test con email specifica
python test_sendgrid.py tua-email@example.com
```

## Funzionalità Email Attive

Il sistema utilizza l'email per:

- **Reset Password**: Quando un utente richiede il reset della password tramite `/auth/landing/reset-password`
- **Report Settimanali**: (se configurato nei job)

## Verifiche di Sicurezza

- ✅ API Key SendGrid configurata
- ✅ SMTP over TLS (porta 587)
- ✅ Email mittente configurata: `danielepili@react-company.com`
- ✅ Autenticazione tramite API Key

## Troubleshooting

### Errore "SMTP not configured"
- Verifica che tutte le variabili d'ambiente siano impostate
- Controlla che il server sia riavviato dopo aver aggiunto le variabili

### Errore durante l'invio
- Verifica che l'API Key SendGrid sia valida
- Controlla che il dominio mittente sia verificato in SendGrid
- Verifica la connessione internet del server

### Test della Configurazione
```python
from server.config import settings
print(f"SMTP configured: {bool(settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASS)}")
```

## Note Importanti

1. **API Key**: La stessa API Key viene utilizzata come password SMTP
2. **Dominio Mittente**: Assicurati che `danielepili@react-company.com` sia verificato in SendGrid
3. **Rate Limiting**: SendGrid ha limitazioni sul numero di email inviabili
4. **Monitoraggio**: Monitora i log di SendGrid per problemi di delivery

## File Modificati

- `server/config.py` - Aggiunta `SMTP_FROM`
- `server/email.py` - Utilizzo di `SMTP_FROM`
- `sendgrid_config.txt` - File di configurazione di riferimento
- `test_sendgrid.py` - Script di test
- `SENDGRID_SETUP.md` - Questa documentazione
