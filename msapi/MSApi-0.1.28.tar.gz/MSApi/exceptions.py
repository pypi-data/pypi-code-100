
class MSApiException(Exception):
    pass


class MSApiHttpException(MSApiException):
    def __init__(self, response):
        self.errors = []
        self.status_code = response.status_code
        if self.status_code in [503]:
            self.errors.append(str(response.text()))
        else:
            json = response.json()
            if json is list:
                for local in json:
                    for json_error in local.get('errors'):
                        self.errors.append(json_error.get('error'))
            else:
                for json_error in json.get('errors'):
                    self.errors.append(json_error.get('error'))

    def __str__(self):
        return 'search={0}'.format("\n".join(self.errors))
