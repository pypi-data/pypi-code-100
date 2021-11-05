from django.urls import path
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from banjo import http
from banjo import views
from banjo.forms import ApiRouteForm
import json

urlpatterns = [
    path("api", views.api, name="api"),
    path("api.json", views.api_json, name="api_json"),
]
user_defined_routes = []

def validate_args(args):
    """Checks that args (the param type signature) is valid.
    """
    if args is None: return
    allowed_types = [str, bool, int, float]
    if not isinstance(args, dict):
        raise ValueError("args must be a dict if provided")
    for param, type_ in args.items():
        if type_ not in allowed_types:
            raise ValueError("param {} in args must be one of: {}".format(
                    param, ', '.join(str(t) for t in allowed_types)))

def create_view(fn, method, args=None):
    """Creates a django view function.
    The view function checks that the HTTP method is correct, 
    extracts the request's params, passes them to `fn`, 
    and returns the result. Args, if provided, should be 
    a dict of {param_name: type}, where type is in 
    [str, bool, int, float].
    """
    def view(request):
        if request.method != method:
            return HttpResponseNotAllowed([method])  
        if args:
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body.decode("utf-8"))
            elif method == 'GET':
                data = request.GET
            else:
                data = request.POST
        FormClass = ApiRouteForm.for_args(args)
        form = FormClass(data)
        if form.is_valid():
            try:
                result = fn(form.cleaned_data)
                return JsonResponse(result)
            except http.BadRequest as e:
                return JsonResponse({'error': str(e)}, status=e.status_code)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    view.__name__ = fn.__name__
    view.__doc__ = fn.__doc__
    validate_args(args)
    view.args = args or {}
    return view

def create_api_view(url, fn, method, args=None):
    """Creates an API view.
    An API view responds to GET requests with a HTML template--
    the response data for GET routes and a form for POST routes.
    For POST routes, the view processes the form.
    """
    def api_view(request):
        fn.args = args or {}
        route = views.describe_route(path(url, fn, name=fn.__name__))

        if method == "GET" and request.method == "GET":
            if args:
                form = ApiRouteForm.for_args(args)(request.GET)
                if form.is_valid():
                    result = fn(form.cleaned_data)
                else:
                    result = None
            else:
                form = None
                result = fn({})
            return render(request, "banjo/api_get.html", {
                "route": route,
                "result": json.dumps(result, indent=True) if result else None,
                "form": form,
            })
        if method == "POST":
            if request.method == "POST":
                if args:
                    form = ApiRouteForm.for_args(args)(request.POST)
                    if form.is_valid():
                        result = fn(form.cleaned_data)
                        form = ApiRouteForm.for_args(args)()
                    else:
                        result = None
                else:
                    form = None
                    result = fn({})
            else:
                if args:
                    form = ApiRouteForm.for_args(args)()
                else:
                    form = None
                result = None

            return render(request, "banjo/api_post.html", {
                "route": route,
                "result": json.dumps(result, indent=True) if result else None,
                "form": form,
            })

        return HttpResponseNotAllowed([request.method])

    api_view.__name__ = fn.__name__
    api_view.__doc__ = fn.__doc__
    validate_args(args)
    api_view.args = args or {}
    return api_view
    

def route_get(url, args=None):
    def bind_url_to_view(fn):
        view = create_view(fn, "GET", args=args)
        api_view = create_api_view(url, fn, "GET", args=args)
        urlpatterns.append(path(url, view, name=view.__name__))
        urlpatterns.append(path("api/" + url, api_view, name="api_" + view.__name__))
        user_defined_routes.append(path(url, view, name=view.__name__))
        return view
    return bind_url_to_view

def route_post(url, args=None):
    def bind_url_to_view(fn):
        view = create_view(fn, "POST", args=args)
        api_view = create_api_view(url, fn, "POST", args=args)
        urlpatterns.append(path(url, view, name=view.__name__))
        urlpatterns.append(path("api/" + url, api_view, name="api_" + view.__name__))
        user_defined_routes.append(path(url, view, name=view.__name__))
        return view
    return bind_url_to_view
