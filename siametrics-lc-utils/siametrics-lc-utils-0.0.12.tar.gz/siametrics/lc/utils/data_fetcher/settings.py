from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = 'dev'

    AWS_REGION: str = 'ap-southeast-1'

    S3_BUCKET_NAME: str = 'lc-data-fetcher'
    DYNAMODB_STATE_TABLE_NAME: str = 'data-fetcher-state'

    AWS_DYNAMODB_KEY: str = None
    AWS_DYNAMODB_SECRET: str = None

    AWS_S3_KEY: str = None
    AWS_S3_SECRET: str = None


settings = Settings()
