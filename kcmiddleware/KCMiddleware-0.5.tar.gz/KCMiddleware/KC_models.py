class KeycloakUser:
    def __init__(self, kc_id, email, first_name, last_name, userinfo, token, current_client):
        self.id = kc_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.userinfo = userinfo
        self.token = token
        self.current_client = current_client
