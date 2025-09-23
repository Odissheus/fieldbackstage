from fastapi import APIRouter, Depends
import uuid
import boto3
from botocore.client import Config
from config import settings
from deps import rate_limit


router = APIRouter(tags=["upload"])


@router.post("/upload/presign")
def presign(body: dict, _rl=Depends(rate_limit(settings.RATE_LIMIT_UPLOAD_PER_MIN))):
    filename = body.get("filename", "file")
    mime = body.get("mime", "application/octet-stream")
    key = f"uploads/{uuid.uuid4()}-{filename}"
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name=settings.S3_REGION,
    )
    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": key, "ContentType": mime},
        ExpiresIn=900,
    )
    return {"url": url, "fields": {"key": key, "Content-Type": mime}}

