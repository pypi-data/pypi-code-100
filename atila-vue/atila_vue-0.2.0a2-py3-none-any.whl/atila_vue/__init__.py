__version__ = "0.2.0a2"

import os
import json
import atila
import skitai
from skitai.wastuff.api import ISODateTimeWithOffsetEncoder
import re

RX_SPACE = re.compile (r'\s+')
ROUTES_CACHE = {}
VIEWS_DIR = "/apps"

class User:
    def __init__ (self, claims):
        self.claims = claims
        self.uid = claims ['uid']
        self.grp = claims ['grp']
        self.tuid = None

    def __getattr__ (self, attr):
        try:
            return self.claims [attr]
        except KeyError:
            raise AttributeError

    def __str__ (self):
        return self.uid


def __config__ (pref):
    pref.config.MINIFY_HTML = 'strip'


def __setup__ (app, mntopt):
    from skitai.wastuff import sendmail

    if "SMTP" in app.config:
        smtp = app.config.SMTP
        sendmail.configure (smtp ["SMTP_SERVER"], smtp ["SMTP_AUTH"], smtp ["SMTP_SENDER"])

    @app.permission_handler
    def permission_handler (was, perms):
        if was.request.get_header ('authorization'):
            was.request.user = None
            claims = was.dejwt ()
            if "err" in claims:
                raise was.Error ("401 Unauthorized", claims ["err"])
            was.request.user = User (claims)

        if 'uid' in was.request.PARAMS:
            tuid = was.request.PARAMS ['uid']
            if 'owner' in perms and tuid != 'me':
                raise was.Error ("403 Permission Denied", "owners only operation")
            was.request.user.tuid = (tuid == 'me' and was.request.user.uid or (tuid != 'notme' and tuid or None))

        if not perms:
            return

        if was.request.user.grp == "staff":
            return # always vaild
        if "staff" in perms:
            raise was.Error ("403 Permission Denied")

    @app.route ('/status')
    @app.permission_required (skitai.isdevel () and ['user'] or ['staff'])
    def status (was, f = ''):
        return was.status (f)

    # template globals ------------------------------------
    @app.template_global ('raise')
    def raise_helper (was, msg):
        raise Exception (msg)

    @app.template_global ('get_apispecs')
    def get_apispecs (was):
        return { k.replace ('.', '_').upper (): v for k, v in sorted (app.get_urlspecs ().items (), key = lambda x: x [0]) if k.startswith ('api') }

    @app.template_global ('build_routes')
    def build_routes (was, base):
        def collect (start, base_len):
            pathes = []
            for fn in os.listdir (start):
                path = os.path.join (start, fn)
                if fn in ('components', 'layout.vue'):
                    continue
                if fn.startswith ('__'):
                    continue

                if os.path.isdir (path):
                    pathes.extend (collect (path, base_len))
                elif fn.endswith ('.vue'):
                    pathes.append ((
                        path [base_len:-4].replace ("\\", '/').replace ('/_', '/:'),
                        path [base_len:].replace ("\\", '/'),
                    ))
            return pathes

        def find (root, meta):
            if not os.path.isdir (root):
                return None, []

            routes = []
            pathes = []
            names = set ()
            for path, vue in collect (root, len (root)):
                if path.endswith ('/index'):
                    path = path [:-6] or '/'
                vue_path = "{}{}{}".format (VIEWS_DIR, base, vue)

                current_meta = {}
                for k, v in meta.items ():
                    if path.startswith (k):
                        current_meta.update (v)
                routes.append ('{name: "%s", path: "%s", component: () => loadModule("%s", options), meta: %s}' % (path [1:] or 'index', path, vue_path, json.dumps (current_meta)))
                if path == '/':
                    was.push (vue_path) # server push
                else:
                    pathes.append (vue_path) # prefetch
            routes_list = ",\n ".join (routes)
            return routes_list, pathes

        global ROUTES_CACHE

        if not app.debug and base in ROUTES_CACHE:
            return ROUTES_CACHE [base]

        if "STATIC_PATH" in app.config:
            static_path = app.config.STATIC_ROOT
        else:
            static_path = os.path.join (app.home, 'static') # default

        current = os.path.join (static_path, VIEWS_DIR [1:], base [1:])
        meta = {}
        meta_file = os.path.join (current, 'meta.json')
        if os.path.isfile (meta_file):
            with open (meta_file) as f:
                meta = json.loads (f.read ())

        routes_list, pathes = find (current, meta)

        layout = os.path.join (VIEWS_DIR [1:], base [1:], 'layout.vue')
        assert os.path.isfile (os.path.join (static_path, layout)), 'layout.vue is missing'

        if not routes_list:
            home = os.path.join (os.path.dirname (__file__), '../static', VIEWS_DIR [1:], base [1:])
            routes_list, pathes = find (home)

        assert routes_list, 'no page components for vue-router'
        assert 'name: "index"' in routes_list, 'index.vue is missing'

        ROUTES_CACHE [base] = (routes_list, pathes, layout)
        return routes_list, pathes, layout

    # template filters --------------------------------------
    @app.template_filter ('vue')
    def vue (val):
        return '{{ %s }}' % val

    @app.template_filter ('summarize')
    def summarize (val, chars = 60):
        if not val:
            return ''
        s = val.find (" ", chars)
        if s == -1:
            return RX_SPACE.sub (" ", val.strip ())
        else:
            return RX_SPACE.sub (" ", val.strip () [: min (s, chars + 10)]) + '...'

    @app.template_filter ('attr')
    def attr (val):
        if not val:
            return '""'
        return '"{}"'.format (val.replace ('"', '\\"'))

    @app.template_filter ('upselect')
    def upselect (val, *names, **upserts):
        d = {}
        for k, v in val.items ():
            if k in names:
                d [k] = v
        d.update (upserts)
        return d

    @app.template_filter ('tojson_with_datetime')
    def tojson_with_datetime (data):
        return json.dumps (data, cls = ISODateTimeWithOffsetEncoder, ensure_ascii = False)


def __mount__ (app, mntopt):
    @app.route ('/base-template')
    def base_template (was):
        import atila_vue
        return f'<h1>Atila Vue Template {atila_vue.__version__}</h1>'
