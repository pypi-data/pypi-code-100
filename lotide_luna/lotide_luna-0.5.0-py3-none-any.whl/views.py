from http import HTTPStatus
from json import loads

from django.shortcuts import redirect, render

from .utils import (
    authenticated_request, get_minimal_post, handle_error, prepare_context)


def index(request):
    """Return default feed: all posts."""
    instance = request.COOKIES.get('instance')
    context = prepare_context(request)
    if instance is None:
        return render(request, 'index.html', context)
    return redirect('timeline', 'home')


def timeline(request, timeline_type='all', page=None):
    """View timeline of posts.

    timeline_type: string
        `all`: all posts from local and connected instances
        `local`: only posts from local instance
        `home`: posts from communities the user follow

    page: string
        the page ID assigned by lotide
    """
    context = prepare_context(request)
    endpoint = '/posts?limit=20'
    if timeline_type == 'local':
        endpoint += '&in_any_local_community=true'
    elif timeline_type == 'home':
        endpoint += '&include_your_follow=true'
    if page is not None:
        endpoint += f'&page={page}'
    response = authenticated_request(request, 'GET', endpoint)
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    json = response.json()
    context['posts'] = [get_minimal_post(post) for post in json['items']]
    context['timeline_type'] = timeline_type
    context['next_page'] = json['next_page']
    return render(
        request, 'timeline.html', context)


def list_communities(request):
    """View list of communities."""
    context = prepare_context(request)
    response = authenticated_request(request, 'GET', '/communities')
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    communities = response.json()['items']
    context['local'] = [community for community in communities
                        if community['local']]
    context['remote'] = [community for community in communities
                         if not community['local']]
    return render(request, 'communities.html', context)


def community(request, community_id, page=None):
    """View community and its posts."""
    context = prepare_context(request)
    community_response = authenticated_request(
        request, 'GET', f'/communities/{community_id}')
    if community_response.status_code != HTTPStatus.OK:
        return handle_error(community_response)
    timeline_url = f'/posts/?community={community_id}'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = authenticated_request(request, 'GET', timeline_url)
    if timeline_response.status_code != HTTPStatus.OK:
        return handle_error(timeline_response)

    json = timeline_response.json()
    context['community'] = community_response.json()
    context['posts'] = [get_minimal_post(post) for post in json['items']]
    context['timeline_type'] = 'community',
    context['next_page'] = json['next_page']

    return render(request, 'community.html', context)


def user(request, user_id, page=None):
    """View user and their posts."""
    context = prepare_context(request)
    user_response = authenticated_request(request, 'GET', f'/users/{user_id}')
    if user_response.status_code != HTTPStatus.OK:
        return handle_error(user_response)
    timeline_url = f'/users/{user_id}/things'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = authenticated_request(request, 'GET', timeline_url)
    if timeline_response.status_code != HTTPStatus.OK:
        return handle_error(timeline_response)
    context['user'] = user_response.json()
    timeline_json = timeline_response.json()
    context['items'] = timeline_json['items']
    context['next_page'] = timeline_json['next_page']
    context['timeline_type'] = 'user',
    return render(request, 'user.html', context)


def post(request, post_id):
    """View post and its comment."""
    context = prepare_context(request)
    post_response = authenticated_request(request, 'GET', f'/posts/{post_id}')
    if post_response.status_code != HTTPStatus.OK:
        return handle_error(post_response)
    comment_response = authenticated_request(
        request, 'get', f'/posts/{post_id}/replies')
    if comment_response.status_code != HTTPStatus.OK:
        return handle_error(comment_response)
    comment_json = comment_response.json()
    context['post'] = post_response.json()
    context['comments'] = comment_json['items']
    context['next_page'] = comment_json['next_page']
    return render(request, 'post.html', context)


def new_post(request, community_id):
    context = prepare_context(request)
    context['community_id'] = community_id
    if request.method == 'GET':
        return render(request, 'new-post.html', context)
    content = request.POST['content-type']
    payload = {
        'community': community_id,
        'href': request.POST['url'],
        'title': request.POST['title'],
        content: request.POST['text'],
    }
    response = authenticated_request(request, 'POST', '/posts', json=payload)
    if response.status_code != HTTPStatus.OK:  # TODO: It should be CREATED, talk with lotide dev
        return handle_error(response)
    post_id = loads(response.content)['id']
    return redirect('post', post_id)


def settings(request):
    """Setting client preferences."""
    context = prepare_context(request)
    if request.method == 'GET':
        return render(request, 'settings.html', context)
    theme = request.POST['theme']
    response = redirect('settings')
    response.set_cookie('luna-theme', theme)
    return response


def login(request):
    """View for login form."""
    theme = request.COOKIES.get('luna-theme', 'auto')
    if request.method == 'GET':
        request.session.set_test_cookie()
        return render(request, 'login.html', {'luna_theme': theme})
    username = request.POST['username']
    instance = request.POST['instance']
    password = request.POST['password']
    payload = {
        'username': username,
        'password': password
    }
    response = authenticated_request(request, 'POST', '/logins',
                                     instance=instance, json=payload)
    json = response.json()
    cookies = {
        'username': username,
        'instance': instance,
        'token': json['token'],
        'user_id': json['user']['id'],
        'is_site_admin': json['user']['is_site_admin'],
        'has_unread_notifications': json['user']['has_unread_notifications']
    }
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = redirect('index')
        for k, v in cookies.items():
            response.set_cookie(k, v)
        return response
    else:
        return render('error/no_cookie.html')


def logout(request):
    """Log out endpoint."""
    response = authenticated_request(request, 'DELETE', '/logins/~current')
    response = redirect('index')
    cookies = [
        'username',
        'instance',
        'token',
        'user_id',
        'is_site_admin',
        'has_unread_notifications'
    ]
    for cookie in cookies:
        response.delete_cookie(cookie)
    return response
