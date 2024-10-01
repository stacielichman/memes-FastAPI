from contextlib import suppress

import boto3
from botocore.exceptions import NoCredentialsError, ClientError, BotoCoreError
from fastapi import UploadFile

from app.core.config import settings

minio_client = boto3.client(
    's3',
    endpoint_url=settings.MINIO_URL,
    aws_access_key_id=settings.MINIO_ROOT_USER,
    aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
)

with suppress(ClientError):
    minio_client.create_bucket(Bucket=settings.MINIO_BUCKET_NAME)


def upload_file_to_minio(file: UploadFile) -> str:
    """
    Uploads a file to MinIO storage.

    Args:
        file: The file to upload

    Returns:
        The URL of the uploaded file

    Raises:
        Exception: If there's an error during upload
    """
    try:
        file_data = file.file
        file_name = file.filename
        minio_client.upload_fileobj(file_data, settings.MINIO_BUCKET_NAME, file_name)
        file_url = f"{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{file_name}"
        return file_url
    except NoCredentialsError:
        raise Exception("Credentials not available")
    except (ClientError, BotoCoreError) as e:
        raise Exception(f"Error uploading file: {e}")
