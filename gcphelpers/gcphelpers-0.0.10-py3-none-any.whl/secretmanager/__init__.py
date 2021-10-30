from google.cloud import secretmanager

def access_secret_manager_secret(secretRef, project, version="latest"):
    """
    Access a secret from Google Secret Manager
    :param string secretRef: A Secret Manager secret name
    :param string project: GCP project name or project ID
    :param string version: Define a specific version to use, otherwise use latest
    :return: A plaintext secret value
    """ 
    client   = secretmanager.SecretManagerServiceClient()
    secret   = f"projects/{project}/secrets/{secretRef}/versions/{version}"

    try:
        response = client.access_secret_version(request={
            "name": secret
        })
    except Exception as e:
        return e

    return response.payload.data.decode("UTF-8")