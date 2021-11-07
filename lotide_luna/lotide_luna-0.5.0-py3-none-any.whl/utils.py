from http import HTTPStatus

import requests
from django.http import HttpResponse


def get_fedi_name(name, instance, local):
    """Turn username to fediverse style."""
    if local:
        return name
    else:
        return f'{name}@{instance}'


def get_minimal_post(post):
    """Get only essential information for a post preview."""
    return {
        'url': f'/posts/{post["id"]}',
        'title': post['title'],
        'created': post['created'],
        'author': get_fedi_name(
            post['author']['username'],
            post['author']['host'],
            post['author']['local']),
        'author_url': f'/users/{post["author"]["id"]}',
        'community': get_fedi_name(
            post['community']['name'],
            post['community']['host'],
            post['community']['local']),
        'community_url': f'/communities/{post["community"]["id"]}'
    }


def handle_error(response):
    """Return uniform HTTP response."""
    response = HttpResponse(
        'Some error occured when trying to retrieve data',
        headers=response.headers
    )
    response.status_code = response.status_code
    return response


def prepare_context(request, **kwargs):
    """Prepare a context object with necessary information for rendering."""
    theme = request.COOKIES.get('luna-theme', 'auto')
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')

    context = {'luna_theme': theme}
    if username is not None and user_id is not None:
        context['logged_in'] = {'username': username, 'id': user_id}

    for k, v in kwargs.items():
        context[k] = v
    return context


def authenticated_request(request, method, path, instance=None, **kwargs):
    """Short hand for ensuring a request is made while authenticated."""
    if instance is None:
        instance = request.COOKIES.get('instance')
    token = request.COOKIES.get('token')
    BASE_URL = 'https://%s/api/unstable'
    method = method.lower()
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    full_path = f'{BASE_URL % instance}{path}'
    if token is not None:
        kwargs['headers'] = {'Authorization': f'Bearer {token}'}
    if method == 'get':
        return requests.get(full_path, **kwargs)
    elif method == 'post':
        return requests.post(full_path, **kwargs)
    elif method == 'put':
        return requests.put(full_path, **kwargs)
    elif method == 'delete':
        return requests.delete(full_path, **kwargs)
