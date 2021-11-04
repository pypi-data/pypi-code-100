from django.contrib.auth import get_user_model, login


def suap_ead_user(user, profile=None):
    return {'user': user, 'profile': profile}


class PreExistentUserJwtBackend:
    def login_user(self, request, user_data):
        user = get_user_model().objects.get(username=user_data['username'])
        login(request, user, backend=None)
        request.session['suap_ead'] = suap_ead_user(user_data)


class CreateNewUserJwtBackend:
    def login_user(self, request, user_data):
        user, created = get_user_model().objects.get_or_create(username=user_data['username'])
        login(request, user, backend=None)
        request.session["suap_ead"] = suap_ead_user(user_data)
