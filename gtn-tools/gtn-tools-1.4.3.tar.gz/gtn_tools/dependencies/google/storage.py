from google.cloud import storage
from gtn_tools.schemas.transcription_schemas import TranscriptionInputFile


def upload_blob(bucket_name: str, file: TranscriptionInputFile) -> bool:
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.file)

    return 'gs://' + bucket_name + '/' + file.filename


def delete_blob(bucket_name: str, blob_name: str) -> bool:
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    return True
