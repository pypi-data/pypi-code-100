from fitbit_downloader.config import Config
from fitbit_downloader.download import download_data


def main():
    config = Config.load_recursive()
    download_data(config)


if __name__ == "__main__":
    main()
