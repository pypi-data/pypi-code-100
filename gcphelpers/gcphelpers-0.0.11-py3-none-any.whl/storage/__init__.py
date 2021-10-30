from google.cloud import storage

def push_object_to_gcs_bucket_from_stream(bytestream, fileName, bucketId, contentType="text/plain"):
    """
    Push a bucket object containing a bytestream
    Can be used for plaintext, ZIP archives, music files, anything that can be a bytestream
    :param object bytestream: File content
    :param string fileName: Created file name
    :param string bucketId: A GCP bucket ID
    :param string contentType: Content-Type header content https://www.iana.org/assignments/media-types/media-types.xhtml
    """
    client = storage.Client()
    bucket = client.get_bucket(bucketId)
    blob   = bucket.blob(fileName)
    
    try:
        blob.upload_from_string(bytestream, content_type=contentType)
    except Exception as e:
        return e

    return "OK"