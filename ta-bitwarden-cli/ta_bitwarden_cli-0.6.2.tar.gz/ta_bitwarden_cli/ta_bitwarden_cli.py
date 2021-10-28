import os
import subprocess
import json
import logging

from .download_bitwarden import DownloadBitwarden


class Bitwarden(object):
    """
    Main class that does all work
    """

    def __init__(self, bitwarden_credentials=None):
        """
        bitwarden_credentials - dict with 'password' / 'client_id' / 'client_secret' keys
        'bw' binary should be already in PATH
        """
        self.data = {}
        self.path_to_exe_file = "bw"
        self.bitwarden_credentials = bitwarden_credentials
        self.bitwarden_token = ""

        self.bitwarden_exe("logout")

    def bitwarden_exe(self, *command):
        """
        Provide coma-separated command line arguments that you want to provide to bw CLI binary
        Searches binary in PATH. If fails tries to run it from current working directory
        Examples:
          - bw.bitwarden_exe('logout')
          - bw.bitwarden_exe(
            "unlock",
            self.bitwarden_credentials["password"],
            "--raw",
            )
        """
        env = {
            **os.environ,
        }

        if (
            self.bitwarden_credentials["client_id"]
            and self.bitwarden_credentials["client_secret"]
        ):
            env["BW_CLIENTID"] = str(self.bitwarden_credentials["client_id"])
            env["BW_CLIENTSECRET"] = str(self.bitwarden_credentials["client_secret"])
            logging.info("Using provided client_id and client_secret")
        else:
            logging.info("Using client_id and client_secret from env vars")

        try:
            return subprocess.run(
                [
                    self.path_to_exe_file,
                    *command,
                ],
                capture_output=True,
                text=True,
                timeout=180,
                env=env,
            )
        except FileNotFoundError:
            self.path_to_exe_file = DownloadBitwarden.download_bitwarden()
            return subprocess.run(
                [
                    self.path_to_exe_file,
                    *command,
                ],
                capture_output=True,
                text=True,
                timeout=180,
                env=env,
            )

    def bitwarden_login(self):
        """
        Performs login opeartion via BitWarden CLI
        Requires password / client_id / client_secret already set when creation Bitwarden instance
        """
        bitwarden_app = self.bitwarden_exe(
            "login",
            "--apikey",
        )

        if "You are logged in!" in bitwarden_app.stdout:
            bitwarden_app = self.bitwarden_exe(
                "unlock",
                self.bitwarden_credentials["password"],
                "--raw",
            )
            self.bitwarden_token = bitwarden_app.stdout
            if "Invalid master password" in self.bitwarden_token:
                logging.error(bitwarden_app.stdout)
                raise Exception("Invalid master password!")
        else:
            logging.error(bitwarden_app.stdout)
            raise Exception("Failed to login via api key!")

    def get_credentials(self, user_credentials_name):
        """
        This method is for backward compatibility
        """
        self.bitwarden_login()
        self.get_data(user_credentials_name)
        return self.data

    def get_data(self, data):
        """
        Core method
        Obtaining of data from bitwarden vault for provided Key Name
        Saves dict with results to self.data variable
        Each key in dict is your custom name
        Each value in dict is another dict with data from bitwarden vault

        Example:

          creds = {
              "unicourt_api": "UniCourt API",
              "unicourt_alpha_api": "UniCourt Alpha API Dev Portal",
              "aws": "AWS Access Key & S3 Bucket",
          }
          bw.get_data(creds)
          assert isinstance(bw.data['aws'],dict)
        """
        print("Getting bitwarden data...")
        bitwarden_app = self.bitwarden_exe(
            "list",
            "items",
            "--session",
            self.bitwarden_token,
        )

        if not bitwarden_app.stdout:
            raise Exception("Empty items list! Probably some issue with loggin in")

        bitwarden_items = json.loads(bitwarden_app.stdout)
        for credentials_key, credentials_name in data.items():
            for bw_item in bitwarden_items:
                if credentials_name == bw_item["name"]:
                    self.data[credentials_key] = {}
                    self.data[credentials_key]["login"] = bw_item["login"]["username"]
                    self.data[credentials_key]["password"] = bw_item["login"][
                        "password"
                    ]
                    if "uris" in bw_item["login"]:
                        self.data[credentials_key]["url"] = bw_item["login"]["uris"][0][
                            "uri"
                        ]
                    else:
                        self.data[credentials_key]["url"] = ""
                    if bw_item["login"]["totp"] is None:
                        self.data[credentials_key]["otp"] = ""
                    else:
                        bitwarden_app = self.bitwarden_exe(
                            "get",
                            "totp",
                            bw_item["id"],
                            "--session",
                            self.bitwarden_token,
                        )
                        self.data[credentials_key]["otp"] = bitwarden_app.stdout
                    if "fields" in bw_item:
                        for field in bw_item["fields"]:
                            self.data[credentials_key][field["name"]] = field["value"]
        if len(self.data) != len(data):
            logging.error("Can't get data from bitwarden")
            raise Exception("Bitwarden ERROR")
        self.bitwarden_exe("logout")
