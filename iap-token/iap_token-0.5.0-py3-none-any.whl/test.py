import iap_token
import os

def test_logging():
    print(iap_token.get_token())
    print(iap_token.get_token(os.environ["MLFLOW_TRACKING_URI"]))

if __name__ == "__main__":
    test_logging()
