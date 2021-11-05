class BoardRsconnect(Board):
    """
    Create a new pins board object
    """

    def __init__(self, connect_server, api_key):
        self.board_type = "RStudio Connect"
        self.connect_server = connect_server
        self.api_key = api_key
        self.auth_header = {"Authorization": "Key " + api_key}
        self.temp_dir = tempfile.TemporaryDirectory()
        Board.__init__(self, self.board_type)

    def _write_data(self, data):
        # Write out the data
        data.to_json(self.temp_dir.name + "/data.txt")

    def _write_index(self, pin_display_name):
        # Write out the landing page
        lines = [
            "<h1 style='font-family: sans-serif'>Python Pin: " + pin_display_name + "</h1>\n",
            "<p style='font-family: sans-serif'>Created with version "
            + metadata.version("pins")
            + " of the python pins package.<br>\n",
            "See <a href='https://pypi.org/project/pins/' target='_blank'>"
            + "https://pypi.org/project/pins/</a> for more info.</p>\n",
        ]
        with open(self.temp_dir.name + "/index.html", "w") as index_file:
            for line in lines:
                index_file.write(line)

    def _write_manifest(self):
        # Write out the manifest
        manifest = {
            "version": 1,
            "locale": "en_US",
            "platform": "3.5.1",
            "metadata": {
                "appmode": "static",
                "primary_rmd": None,
                "primary_html": "index.html",
                "content_category": "pin",
                "has_parameters": False,
            },
            "packages": None,
            "files": None,
            "users": None,
        }
        with open(self.temp_dir.name + "/manifest.json", "w") as manifest_file:
            json.dump(manifest, manifest_file)

    def _get_content(self, pin_name, pin_display_name):
        content = req.get(
            self.connect_server + "/__api__/v1/content",
            headers=self.auth_header,
            params={"name": pin_name},
        ).json()
        if content:  # if content item already exists
            return content[0]
        data = {"access_type": "acl", "name": pin_name, "title": pin_display_name}
        content = req.post(
            self.connect_server + "/__api__/v1/content",
            headers=self.auth_header,
            json=data,
        ).json()
        return content

    def _create_upload_and_deploy(self, pin_name, pin_display_name):
        # Turn into tarfile
        temp_tarfile = tempfile.NamedTemporaryFile()
        with tarfile.open(temp_tarfile.name, "w:gz") as tar:
            tar.add(self.temp_dir.name, arcname=os.path.basename(self.temp_dir.name))

        content = self._get_content(pin_name, pin_display_name)
        content_url = self.connect_server + "/__api__/v1/content/" + content["guid"]

        # Upload Bundle
        with open(temp_tarfile.name, "rb") as file_conn:
            bundle = req.post(
                content_url + "/bundles", headers=self.auth_header, data=file_conn
            )
        bundle_id = bundle.json()["id"]

        # Deploy bundle
        _deploy = req.post(
            content_url + "/deploy",
            headers=self.auth_header,
            json={"bundle_id": bundle_id},
        )
        return {
            "dash_url": content["dashboard_url"],
            "content_url": content["content_url"],
        }

    def push_pin(self, data, pin_name, pin_display_name):
        """
        Pushes data to an RStudio Connect board
        """
        self._write_data(data)
        self._write_index(pin_display_name)
        self._write_manifest()
        output = self._create_upload_and_deploy(pin_name, pin_display_name)
        return output

    def get_pin(self, content_url):
        """
        Pulls pins data from an RStudio Connect board
        """
        res = req.get(
            content_url + "/data.txt",
            headers=self.auth_header,
        )
        return res.json()
