import os
from tornado import web
from multidict import MultiDict
from tornadmin.utils.template import get_value, get_chained_attr
from tornadmin.utils.text import replace_qs


BASE_DIR = os.path.dirname(__file__)


class AdminUser:
    def __init__(self, username, **kwargs):
        self.username = username
        self.display_name = kwargs.get('display_name', username)

    def __bool__(self):
        if self.username:
            return True
        return False


class BaseHandler(web.RequestHandler):
    admin_site = None

    async def prepare(self):
        auth_data = await self.admin_site.authenticate(self)
        if not auth_data:
            auth_data = {'username': None}

        self.current_user = AdminUser(**auth_data)

        if not self.current_user and getattr(self, 'login_required', True):
            return self.redirect(self.reverse_url('admin:login'))

    def redirect(self, url, *args, **kwargs):
        """Override handler's redirect method to be able to 
        redirect using url names.

        args will be passed to reversing function.
        kwargs will be passed to redirect function.
        """
        if (':' in url):
            # url is a route name
            url = self.reverse_url(url, *args)

        return super().redirect(url, **kwargs)

    def reverse_url(self, name, *args):
        """Override handler's reverse_url to strip question mark
        from the reversed url.
        """

        reversed_url = self.application.reverse_url(name, *[arg for arg in args if arg])
        return reversed_url.strip('?')

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'templates')

    def get_template_namespace(self):
        namespace = super().get_template_namespace()
        namespace.update({
            'get_value': get_value,
            'get_chained_attr': get_chained_attr,
            'replace_qs': replace_qs,
            'admin_site': self.admin_site
        })
        return namespace

    def static_url(self, path, include_host=None, **kwargs):
        """We override RequestHandler's `static_url` to
        use our own static directory path instead of
        the value from `static_path` appication setting.

        :TODO: Provide a setting called `admin_static_path` so user can
        configure admin static files location.
        """
        if path.startswith('tornadmin'):

            get_url = self.settings.get(
                "static_handler_class", StaticFileHandler
            ).make_static_url

            if include_host is None:
                include_host = getattr(self, "include_host", False)

            if include_host:
                base = self.request.protocol + "://" + self.request.host + self.admin_site.base_url
            else:
                base = self.admin_site.base_url

            fake_settings = {
                'static_path': os.path.join(BASE_DIR, 'static'),
            }

            return base + get_url(fake_settings, path, **kwargs)

        else:
            return super().static_url(path, include_host, *args, **kwargs)

    def _static_url(self, path, *args, **kwargs):
        url = super().static_url(path, *args, **kwargs)
        if path.startswith('tornadmin'):
            url = self.admin_site.base_url + url
        return url


class StaticFileHandler(web.StaticFileHandler):
    def initialize(self):
        super().initialize(path=os.path.join(BASE_DIR, 'static'))


class LoginHandler(BaseHandler):
    login_required = False

    async def get(self):
        if self.current_user:
            return self.redirect('admin:index')

        namespace = {
            'error': False,
            'username': ''
        }

        self.render('login.html', **namespace)

    async def post(self):
        if self.current_user:
            return self.redirect('admin:index')

        success = await self.admin_site.login(self)

        if isinstance(success, tuple):
            success, message = success
        else:
            message = 'Wrong username or password'

        if success:
            return self.redirect('admin:index')

        namespace = {
            'error': True,
            'message': message,
            'username': self.get_body_argument('username', '')
        }

        self.render('login.html', **namespace)

class LogoutHandler(BaseHandler):
    login_required = False

    async def post(self):
        if not self.current_user:
            return self.redirect('admin:login')

        success = await self.admin_site.logout(self)
        if success:
            return self.redirect('admin:login')

        self.redirect('admin:index')


class IndexHandler(BaseHandler):
    def get(self):
        registry = []

        _registry = self.admin_site.get_registry()

        for key, admin in _registry.items():
            registry.append(admin)

        namespace = {
            'registry': registry,
        }
        self.render('index.html', **namespace)


class ListHandler(BaseHandler):
    async def get(self, app_slug, model_slug):
        admin = self.admin_site.get_registered(app_slug, model_slug)

        page_num = self.get_query_argument('page', 1)
        q = self.get_query_argument('q', '')

        list_items, page = await admin.get_list(self, page_num=page_num, q=q)

        namespace = {
            'admin': admin,
            'headers': admin.get_list_headers(),
            'list_items': list_items,
            'page': page,
            'q': q,
        }

        self.render('list.html', **namespace)

    async def post(self, app_slug, model_slug):
        admin = self.admin_site.get_registered(app_slug, model_slug)

        action_name = self.get_body_argument('_action')
        selected = self.get_body_arguments('_selected')
        selected_all = self.get_body_argument('_selected_all', False)

        queryset = await admin.get_action_queryset(self, action_name, selected, selected_all)
        action = admin.get_action(self, action_name)

        if action:
            if hasattr(admin, action_name):
                await action(self, queryset)
            else:
                await action(admin, self, queryset)

            if self._finished:
                return

        return self.redirect('admin:list', app_slug, model_slug)


class CreateHandler(BaseHandler):
    async def get(self, app_slug, model_slug):
        admin = self.admin_site.get_registered(app_slug, model_slug)
        form_class = admin.get_form(self)
        form = form_class()
        await form.set_field_choices(self)
        namespace = {
            'obj': None,
            'admin': admin,
            'form': form,
        }
        self.render('create.html', **namespace)

    async def post(self, app_slug, model_slug,):
        admin = self.admin_site.get_registered(app_slug, model_slug)
        form_class = admin.get_form(self)
        
        data = MultiDict()

        for field_name in form_class._fields:
            # :TODO: Implement a multivaluedict to store values in a list
            # instead of using data dictionary
            # because the current way doesn't allow multiple values.
            value = self.get_body_arguments(field_name, None)
            if value:
                data.extend(list(zip([field_name] * len(value), value)))
            else:
                data[field_name] = None

        form = form_class(formdata=data)

        await form.set_field_choices(self)

        if form.validate():
            obj = await admin.save_model(self, form)
            self.redirect('admin:detail', app_slug, model_slug, obj.id)
            return

        namespace = {
            'obj': None,
            'admin': admin,
            'form': form,
        }
        self.render('create.html', **namespace)



class DetailHandler(BaseHandler):
    async def get(self, app_slug, model_slug, id):
        admin = self.admin_site.get_registered(app_slug, model_slug)
        form_class = admin.get_form(self)
        obj = await admin.get_object(self, id)
        data = await admin.get_form_data(obj)

        form = form_class(data=data)
        await form.set_field_choices(self, obj=obj)

        namespace = {
            'obj': obj,
            'admin': admin,
            'form': form,
        }

        self.render('create.html', **namespace)

    async def post(self, app_slug, model_slug, id):
        admin = self.admin_site.get_registered(app_slug, model_slug)
        form_class = admin.get_form(self)
        obj = await admin.get_object(self, id)

        data = MultiDict()

        for field_name in form_class._fields:
            # :TODO: Implement a multivaluedict to store values in a list
            # instead of using data dictionary
            # because the current way doesn't allow multiple values.
            value = self.get_body_arguments(field_name, None)
            if value:
                data.extend(list(zip([field_name] * len(value), value)))
            else:
                data[field_name] = None

        form = form_class(formdata=data)
        await form.set_field_choices(self, obj=obj)

        if form.validate():
            await admin.save_model(self, form, obj)
            if self.get_body_argument('_addanother', False):
                self.redirect('admin:create', app_slug, model_slug)
            else:
                self.redirect('admin:detail', app_slug, model_slug, obj.id)
            return

        namespace = {
            'obj': obj,
            'admin': admin,
            'form': form,
        }

        self.render('create.html', **namespace)


class DeleteHandler(BaseHandler):
    async def post(self, app_slug, model_slug, id):
        admin = self.admin_site.get_registered(app_slug, model_slug)
        form_class = admin.get_form(self)
        obj = await admin.get_object(self, id)

        # :TODO: check if user has delete permission
        await obj.delete()

        self.redirect('admin:list', app_slug, model_slug)