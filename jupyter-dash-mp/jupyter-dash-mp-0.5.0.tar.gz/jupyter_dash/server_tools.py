#THIS CODE IS MODIFIED FROM CORE DASH CODE
from werkzeug.serving import make_server
from werkzeug.debug import DebuggedApplication
from urllib.parse import urlparse
import threading
import os

activeservers = {}

def run_server(
        dashapp,
        host=os.getenv("HOST", "127.0.0.1"),
        port=os.getenv("PORT", "8050"),
        proxy=os.getenv("DASH_PROXY", None),
        debug=False,
        dev_tools_ui=None,
        dev_tools_props_check=None,
        dev_tools_serve_dev_bundles=None,
        dev_tools_hot_reload=None,
        dev_tools_hot_reload_interval=None,
        dev_tools_hot_reload_watch_interval=None,
        dev_tools_hot_reload_max_retry=None,
        dev_tools_silence_routes_logging=None,
        dev_tools_prune_errors=None,
        **flask_run_options,
):
    """Start the flask server in local mode, you should not run this on a
    production server, use gunicorn/waitress instead.
    If a parameter can be set by an environment variable, that is listed
    too. Values provided here take precedence over environment variables.
    :param dashapp: Dash app to serve
    :param host: Host IP used to serve the application
        env: ``HOST``
    :type host: string
    :param port: Port used to serve the application
        env: ``PORT``
    :type port: int
    :param proxy: If this application will be served to a different URL
        via a proxy configured outside of Python, you can list it here
        as a string of the form ``"{input}::{output}"``, for example:
        ``"http://0.0.0.0:8050::https://my.domain.com"``
        so that the startup message will display an accurate URL.
        env: ``DASH_PROXY``
    :type proxy: string
    :param debug: Set Flask debug mode and enable dev tools.
        env: ``DASH_DEBUG``
    :type debug: bool
    :param debug: Enable/disable all the dev tools unless overridden by the
        arguments or environment variables. Default is ``True`` when
        ``enable_dev_tools`` is called directly, and ``False`` when called
        via ``run_server``. env: ``DASH_DEBUG``
    :type debug: bool
    :param dev_tools_ui: Show the dev tools UI. env: ``DASH_UI``
    :type dev_tools_ui: bool
    :param dev_tools_props_check: Validate the types and values of Dash
        component props. env: ``DASH_PROPS_CHECK``
    :type dev_tools_props_check: bool
    :param dev_tools_serve_dev_bundles: Serve the dev bundles. Production
        bundles do not necessarily include all the dev tools code.
        env: ``DASH_SERVE_DEV_BUNDLES``
    :type dev_tools_serve_dev_bundles: bool
    :param dev_tools_hot_reload: Activate hot reloading when app, assets,
        and component files change. env: ``DASH_HOT_RELOAD``
    :type dev_tools_hot_reload: bool
    :param dev_tools_hot_reload_interval: Interval in seconds for the
        client to request the reload hash. Default 3.
        env: ``DASH_HOT_RELOAD_INTERVAL``
    :type dev_tools_hot_reload_interval: float
    :param dev_tools_hot_reload_watch_interval: Interval in seconds for the
        server to check asset and component folders for changes.
        Default 0.5. env: ``DASH_HOT_RELOAD_WATCH_INTERVAL``
    :type dev_tools_hot_reload_watch_interval: float
    :param dev_tools_hot_reload_max_retry: Maximum number of failed reload
        hash requests before failing and displaying a pop up. Default 8.
        env: ``DASH_HOT_RELOAD_MAX_RETRY``
    :type dev_tools_hot_reload_max_retry: int
    :param dev_tools_silence_routes_logging: Silence the `werkzeug` logger,
        will remove all routes logging. Enabled with debugging by default
        because hot reload hash checks generate a lot of requests.
        env: ``DASH_SILENCE_ROUTES_LOGGING``
    :type dev_tools_silence_routes_logging: bool
    :param dev_tools_prune_errors: Reduce tracebacks to just user code,
        stripping out Flask and Dash pieces. Only available with debugging.
        `True` by default, set to `False` to see the complete traceback.
        env: ``DASH_PRUNE_ERRORS``
    :type dev_tools_prune_errors: bool
    :param flask_run_options: Given to `Flask.run`
    :return:
    """
    global activeservers
    dashapp.enable_dev_tools(
        debug,
        dev_tools_ui,
        dev_tools_props_check,
        dev_tools_serve_dev_bundles,
        dev_tools_hot_reload,
        dev_tools_hot_reload_interval,
        dev_tools_hot_reload_watch_interval,
        dev_tools_hot_reload_max_retry,
        dev_tools_silence_routes_logging,
        dev_tools_prune_errors,
    )

    # Verify port value
    try:
        port = int(port)
        assert port in range(1, 65536)
    except Exception as e:
        e.args = [
            "Expecting an integer from 1 to 65535, found port={}".format(repr(port))
        ]
        raise

    # so we only see the "Running on" message once with hot reloading
    # https://stackoverflow.com/a/57231282/9188800
    if os.getenv("WERKZEUG_RUN_MAIN") != "true":
        ssl_context = flask_run_options.get("ssl_context")
        protocol = "https" if ssl_context else "http"
        path = dashapp.config.requests_pathname_prefix

        if proxy:
            served_url, proxied_url = map(urlparse, proxy.split("::"))

            def verify_url_part(served_part, url_part, part_name):
                if served_part != url_part:
                    raise Exception( #I can't get access to dash level exceptions
                        """
                        PROXY ERROR
                        {0}: {1} is incompatible with the proxy:
                            {3}
                        To see your app at {4},
                        you must use {0}: {2}
                    """.format(
                            part_name,
                            url_part,
                            served_part,
                            proxy,
                            proxied_url.geturl(),
                        )
                    )

            verify_url_part(served_url.scheme, protocol, "protocol")
            verify_url_part(served_url.hostname, host, "host")
            verify_url_part(served_url.port, port, "port")

            display_url = (
                proxied_url.scheme,
                proxied_url.hostname,
                (":{}".format(proxied_url.port) if proxied_url.port else ""),
                path,
            )
        else:
            display_url = (protocol, host, ":{}".format(port), path)

        dashapp.logger.info("Dash is running on %s://%s%s%s\n", *display_url)

    if dashapp.config.extra_hot_reload_paths:
        extra_files = flask_run_options["extra_files"] = []
        for path in dashapp.config.extra_hot_reload_paths:
            if os.path.isdir(path):
                for dirpath, _, filenames in os.walk(path):
                    for fn in filenames:
                        extra_files.append(os.path.join(dirpath, fn))
            elif os.path.isfile(path):
                extra_files.append(path)

    if host + ":" + str(port) in activeservers:
        activeservers[host + ":" + str(port)].shutdown()
    app = dashapp.server
    if debug:
        app = DebuggedApplication(app, evalex=True)
    s = make_server(host, port, app, threaded=True)
    t = threading.Thread(target=s.serve_forever)
    t.start()
    activeservers[host + ":" + str(port)] = s