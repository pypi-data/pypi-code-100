import json
import requests
import boto3
import base64
import io
import gzip
from typing import Dict, Union, Sequence, IO, NoReturn


class Coegil:
    def __init__(self, api_key: str, instance_name: str = 'prod', auto_validate: bool = True,
                 proxy_configuration: Dict = None):
        """
        Access the Coegil Public API from code
        Args:
            api_key (str): The API Key
            instance_name (str): The name of the instance.  As Coegil Support for details.
            auto_validate (bool): Run a test to validate the API Key on construction
            proxy_configuration (Dict): Optionally pass proxy config (for the python requests library).
        """
        self._api_key: str = api_key
        self._instance_name = instance_name.lower()
        self._proxy_configuration: Dict = proxy_configuration if proxy_configuration is not None else {}
        if auto_validate:
            self.validate()

    def validate(self):
        """
        Validates your configuration.
        """
        result = self._call_api('GET', '/public/management/key/validate', {})
        return result

    def generate_temporary_api_key(self, duration_hours: int = 36) -> Dict:
        """
        Generates a temporary API key for the given user.  Temporary API keys cannot be used for this API.
        Args:
            duration_hours (int): The length of the key.  The max is 36 hours.

        Returns:
            The temporary API key and expiration info
        """
        result = self._call_api('PUT', '/public/management/key/temporary', {
            'duration_hours': duration_hours
        })
        return result

    def query_database(self, query_text: str, asset_id: str, database_name: str, engine: str = 'my_sql') -> Dict:
        """
        Runs an ad hoc database query.
        Args:
            query_text (str): The query to run.
            asset_id (str): The asset's unique identifier.
            database_name (str): Your database artifact's name.
            engine (str): The database engine (defaults to mysql)
        Returns:
            The results of the query
        """
        result = self._call_api('POST', f'/public/query/{engine}', {
            'asset_id': asset_id,
            'database_name': database_name,
            'query_text': query_text
        })
        return result

    def run_saved_database_query(self, asset_id: str, query_name: str, parameters: Dict = None) -> Dict:
        """
        Runs an ad hoc database query.
        Args:
            asset_id (str): The asset's unique identifier.
            query_name (str): Your saved query's name.
            parameters (Dict): Parameter overrides.
        Returns:
            The results of the query
        """
        result = self._call_api('POST', '/public/query/stored', {
            'asset_id': asset_id,
            'query_name': query_name,
            'query_params': parameters
        })
        return result

    def queue_schedule(self, asset_id: str, job_name: str, schedule_name: str,
                       variable_override: Dict = None) -> NoReturn:
        """
        Queues a job or pipeline schedule to be invoked.  The queue is drained in batches defined by the schedule.
        Args:
            asset_id (str): The asset's unique identifier.
            job_name (str): The name of the job artifact (pipeline, notebook, or trigger).
            schedule_name (str): Required unless you are invoking a trigger.
            variable_override (Dict): Parameter overrides.
        Returns:
        """
        self._call_api('PUT', '/public/schedule/queue', {
            'asset_id': asset_id,
            'job_name': job_name,
            'schedule_name': schedule_name,
            'variable_override': variable_override
        })

    def invoke_schedule(self, asset_id: str, job_name: str, schedule_name: str,
                        variable_override: Dict = None) -> Dict:
        """
        Invoke a job or pipeline schedule.
        Args:
            asset_id (str): The asset's unique identifier.
            job_name (str): The name of the job artifact (pipeline, notebook, or trigger).
            schedule_name (str): Required unless you are invoking a trigger.
            variable_override (Dict): Parameter overrides.
        Returns:
            An identifier to be used for tracking
        """
        return self._call_api('PUT', '/public/schedule', {
            'asset_id': asset_id,
            'job_name': job_name,
            'schedule_name': schedule_name,
            'variable_override': variable_override
        })

    def get_schedule_status(self, job_id: str) -> Dict:
        """
        Gets the status of an invoked job.
        Args:
            job_id (str): The job run id returned from the invoke call.
        Returns:
            The status of the invoked job
        """
        return self._call_api('GET', '/public/schedule/status', {
            'job_id': job_id
        })

    def list_schedules(self, asset_id: str) -> Sequence[Dict]:
        """
        List all of the schedules in a given asset.
        Args:
            asset_id (str): The asset's unique identifier.
        Returns:
            A list of schedules
        """
        return self._call_api('GET', '/public/schedule', {
            'asset_id': asset_id
        })

    def list_artifacts(self, asset_id: str) -> Sequence[Dict]:
        """
        Lists all of the artifacts in a given asset.
        Args:
            asset_id (str): The asset's unique identifier.
        Returns:
            A list of artifacts
        """
        return self._call_api('GET', '/public/artifact', {
            'asset_id': asset_id
        })

    def read_file(self, asset_id: str, artifact_name: str) -> bytes:
        """
        Reads the contents of a file artifact.
        Args:
            asset_id (str): The asset's unique identifier.
            artifact_name (str): The artifact's name.
        Returns:
            A contents of the file
        """
        s3_credentials = self._call_api('GET', '/public/artifact/credentials', {
            'asset_id': asset_id,
            'artifact_name': artifact_name
        })
        s3_bucket = s3_credentials['Bucket']
        s3_key = s3_credentials['Key']
        credential_override = s3_credentials['Credentials']
        return self._get_s3_object(s3_bucket, s3_key, credential_override=credential_override)

    def save_file(self, asset_id: str, artifact_name: str, contents: Union[str, bytes],
                  artifact_sub_type: str = None) -> NoReturn:
        """
        Reads the contents of a file artifact.
        Args:
            asset_id (str): The asset's unique identifier.
            artifact_name (str): The artifact's name.
            contents (Union[str, bytes]): The contents to be uploaded
            artifact_sub_type (str): Optionally pass the artifact sub type.  Talk to Coegil before using this field
        Returns:
            A contents of the file
        """
        self._upload_file(asset_id, artifact_name, contents, artifact_sub_type=artifact_sub_type)

    def _call_api(self, action_method: str, endpoint: str, payload: Dict):
        url = self._build_url(endpoint)
        headers = self._get_headers()
        proxies = self._proxy_configuration
        action_method = action_method.upper()
        if action_method == 'GET':
            r = requests.get(url, headers=headers, params=payload, proxies=proxies)
        elif action_method == 'POST':
            r = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        elif action_method == 'PUT':
            r = requests.put(url, headers=headers, data=json.dumps(payload), proxies=proxies)
        elif action_method == 'DELETE':
            r = requests.delete(url, headers=headers, params=payload, proxies=proxies)
        else:
            raise Exception(f'Unknown action method.  Method={action_method}')
        return self._parse_result(r)

    def _build_url(self, endpoint: str) -> str:
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        instance_name = self._instance_name
        return f'https://api.{instance_name}.app-coegil.com{endpoint}'

    def _parse_result(self, r: requests.Response):
        result = r.json()
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(result) from e
        metadata = result['metaData']
        if metadata['compressData']:
            decompressed_data = self._decompress(result['data'])
        else:
            decompressed_data = result['data']
        return json.loads(decompressed_data)

    def _get_headers(self) -> Dict:
        headers = {
            'api_version': str(2),
            'coegil_api_key': self._api_key,
            'compress_results': str(True)
        }
        return headers

    @staticmethod
    def _decompress(compressed_object: Union[str, bytes]) -> str:
        if isinstance(compressed_object, str):
            compressed_bytes = base64.b64decode(compressed_object)
        else:
            compressed_bytes = compressed_object
        in_ = io.BytesIO()
        in_.write(compressed_bytes)
        in_.seek(0)
        try:
            with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
                gunzipped_bytes_obj = fo.read()

            return gunzipped_bytes_obj.decode()
        except OSError as e:
            if 'Not a gzipped file' in str(e):
                return compressed_object.decode() if isinstance(compressed_object, bytes) else compressed_object
            raise e

    def _upload_file(self, asset_id: str, artifact_name: str, contents: Union[str, bytes], artifact_sub_type: str = None):
        s3_credentials = self._call_api('get', '/public/artifact/credentials', {
            'asset_id': asset_id,
            'artifact_name': artifact_name,
            'artifact_sub_type': artifact_sub_type
        })
        s3_bucket = s3_credentials['Bucket']
        s3_key = s3_credentials['Key']
        artifact_id = s3_credentials['ArtifactGuid']
        credential_override = s3_credentials['Credentials']
        content_type = None
        split_file_name = artifact_name.rsplit('.', 1)
        if len(split_file_name) > 1:
            extension = split_file_name[1]
            if extension == 'xlsx' or extension == 'xls':
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            elif extension == 'ppt' or extension == 'pptx':
                content_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            elif extension == 'docx':
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif extension == 'csv':
                content_type = 'text/csv'
            elif extension == 'json':
                content_type = 'application/json'
            elif extension == 'yml' or extension == 'yaml':
                content_type = 'text/yaml'
        self._put_s3_object(s3_bucket, s3_key, contents, content_type=content_type,
                            credential_override=credential_override)
        self._call_api('POST', '/public/artifact', {
            'asset_id': asset_id,
            'artifacts': [{
                'artifact_name': artifact_name,
                'artifact_type': 'S3',
                'artifact_sub_type': artifact_sub_type,
                'artifact_id': artifact_id
            }]
        })

    def _put_s3_object(self, bucket, key, body: Union[IO, str, bytes], content_type: str = None,
                       credential_override=None):
        client = self._get_client('s3', credential_override)
        if isinstance(body, str):
            body = str.encode(body)
        if isinstance(body, bytes):
            body = io.BytesIO(body)
        params = {
            'ACL': 'private'
        }
        if content_type is not None:
            params['ContentType'] = content_type
        client.upload_fileobj(body, bucket, key, params)

    def _get_s3_object(self, bucket, key, credential_override=None) -> bytes:
        client = self._get_client('s3', credential_override)
        return client.get_object(
            Bucket=bucket,
            Key=key
        ).get('Body').read()

    @staticmethod
    def _get_client(name, credential_override):
        if credential_override is None:
            return boto3.client(name)
        else:
            params = {
                'aws_access_key_id': credential_override['AccessKeyId'],
                'aws_secret_access_key': credential_override['SecretAccessKey'],
            }
            session_token = credential_override.get('SessionToken')
            if session_token is not None:
                params['aws_session_token'] = session_token
            session = boto3.Session(**params)
            client = session.client(name)
            return client
