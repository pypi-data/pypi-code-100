
from urllib.parse import urlparse

import hashlib
import uuid

def infer_id(record_type, record_id, record):

    if not record_type or not record or not isinstance(record, dict):
        return record_id

    record_type = record_type.lower()
    record_type = record_type.replace('schema:', '')

    if record_type == 'webpage':
        new_record_id = _webpage(record_type, record_id, record)
    
    elif record_type == 'website':
        new_record_id = _website(record_type, record_id, record)

    elif record_type == 'image':
        new_record_id = _image(record_type, record_id, record)

    elif record_type == 'organization':
        new_record_id = _organization(record_type, record_id, record)

    elif record_type == 'unknown':
        new_record_id = str(uuid.uuid4())

    elif not record_id:
        new_record_id = str(uuid.uuid4())

    else:
        new_record_id = record_id


    return new_record_id

    

def _webpage(record_type, record_id, record):
    """if @type is webpage
    """

    new_record_id = record_id

    url = record.get('schema:url', None)

    if url:
        new_record_id = _get_url_hash(url)
    

    return new_record_id


def _website(record_type, record_id, record):
    """if @type is webpage
    """
    new_record_id = record_id

    url = record.get('schema:url', None)

    if url:
        domain = urlparse(url).netloc
        new_record_id = _get_url_hash(domain)


    return new_record_id


def _image(record_type, record_id, record):
    """if @type is webpage
    """
    new_record_id = record_id
    url = record.get('schema:url', None)
    contenturl = record.get('schema:contenturl', url)

    if contenturl:
        new_record_id = _get_url_hash(contenturl)

    return new_record_id


def _organization(record_type, record_id, record):
    """if @type is webpage
    """
    new_record_id = record_id
    url = record.get('schema:url', None)
    
    if url:
        domain = urlparse(url).netloc
        new_record_id = _get_url_hash(domain)


    return new_record_id



def _get_url_hash(url):

    if not url:
        return None

    m = hashlib.md5()

    m.update(url.encode('utf-8'))
    result = m.hexdigest()

    return result