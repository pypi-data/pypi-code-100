from boto3.session import Session


_aws_session = Session(
    region_name='eu-central-1',
    aws_access_key_id='AKIAXCSJV3BS6BWMC54H',
    aws_secret_access_key='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'
)


class S3():

    @staticmethod
    def get_secure_url(bucket, filename, expires_in=7200, insecure=False):
        global _aws_session

        # max is 7 days
        if not expires_in:
            expires_in = 7200
        elif expires_in > 604800:
            expires_in = 604800

        url = _aws_session.client('s3').generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket, 'Key': filename},
            ExpiresIn=expires_in
        )

        if insecure:
            return url.split("?")[0]
        else:
            return url
