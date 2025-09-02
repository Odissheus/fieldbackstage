import os


class Settings:
    DB_URL = os.getenv("DB_URL")
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")
    S3_BUCKET_MEDIA = os.getenv("S3_BUCKET_MEDIA", "media")
    # Prefer S3_BUCKET if provided; fallback to legacy S3_BUCKET_MEDIA
    S3_BUCKET = os.getenv("S3_BUCKET", S3_BUCKET_MEDIA)
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_REGION = os.getenv("S3_REGION", "us-east-1")
    S3_SECURE = os.getenv("S3_SECURE", "true").lower() == "true"
    TZ = os.getenv("TZ", "Europe/Rome")
    PURGE_RAW = os.getenv("PURGE_RAW", "true").lower() == "true"
    RAW_WEEKS_TO_KEEP = int(os.getenv("RAW_WEEKS_TO_KEEP", "0"))
    JWT_JWKS_URL = os.getenv("JWT_JWKS_URL")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "fieldback.cloud")
    JWT_TTL_SECONDS = int(os.getenv("JWT_TTL_SECONDS", "86400"))

    SUPERADMIN_USERNAME = os.getenv("SUPERADMIN_USERNAME", "fieldbackmaster")
    SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD", "Leader.1986")
    SUPERADMIN_USER_ID = os.getenv("SUPERADMIN_USER_ID", "00000000-0000-0000-0000-000000000001")

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    SMTP_FROM = os.getenv("SMTP_FROM")
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
    RATE_LIMIT_AUTH_PER_MIN = int(os.getenv("RATE_LIMIT_AUTH_PER_MIN", "30"))
    RATE_LIMIT_UPLOAD_PER_MIN = int(os.getenv("RATE_LIMIT_UPLOAD_PER_MIN", "60"))
    RATE_LIMIT_QA_PER_MIN = int(os.getenv("RATE_LIMIT_QA_PER_MIN", "30"))
    TRUSTED_HOSTS = [h.strip() for h in os.getenv("TRUSTED_HOSTS", "*").split(",") if h.strip()]
    ENFORCE_HTTPS = os.getenv("ENFORCE_HTTPS", "false").lower() == "true"

    # AI/ML Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_WHISPER_MODEL = os.getenv("OPENAI_WHISPER_MODEL", "whisper-1")
    ENABLE_AI_PROCESSING = os.getenv("ENABLE_AI_PROCESSING", "true").lower() == "true"
    TESSERACT_CMD = os.getenv("TESSERACT_CMD")  # Path to tesseract executable
    CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./data/chromadb")


settings = Settings()

