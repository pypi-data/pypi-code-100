from typing import Callable, List

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

from .base_layout import Menu, MenuItem

BootstrapTheme = str


class DashboardApp(Dash):
    def __init__(
        self,
        menu: Menu = [],
        name=None,
        theme: BootstrapTheme = dbc.themes.LUX,
        server=True,
        assets_folder="assets",
        assets_url_path="assets",
        assets_ignore="",
        assets_external_path=None,
        eager_loading=False,
        include_assets_files=True,
        url_base_pathname=None,
        requests_pathname_prefix=None,
        routes_pathname_prefix=None,
        serve_locally=True,
        compress=None,
        meta_tags=None,
        external_scripts=None,
        external_stylesheets=None,
        suppress_callback_exceptions=True,
        prevent_initial_callbacks=False,
        show_undo_redo=False,
        extra_hot_reload_paths=None,
        plugins=None,
        title="Dash",
        update_title="Updating...",
        long_callback_manager=None,
        **obsolete
    ):
        self._menu = menu

        if not external_stylesheets:
            external_stylesheets = [theme]
        else:
            external_stylesheets.insert(0, theme)

        super().__init__(
            name=name,
            server=server,
            assets_folder=assets_folder,
            assets_url_path=assets_url_path,
            assets_ignore=assets_ignore,
            assets_external_path=assets_external_path,
            eager_loading=eager_loading,
            include_assets_files=include_assets_files,
            url_base_pathname=url_base_pathname,
            requests_pathname_prefix=requests_pathname_prefix,
            routes_pathname_prefix=routes_pathname_prefix,
            serve_locally=serve_locally,
            compress=compress,
            meta_tags=meta_tags,
            external_scripts=external_scripts,
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=suppress_callback_exceptions,
            prevent_initial_callbacks=prevent_initial_callbacks,
            show_undo_redo=show_undo_redo,
            extra_hot_reload_paths=extra_hot_reload_paths,
            plugins=plugins,
            title=title,
            update_title=update_title,
            long_callback_manager=long_callback_manager,
            **obsolete
        )

        self.layout = self.create_layout()
        self.register_callbacks()

    @property
    def pages(self) -> List[MenuItem]:
        return [page for item in self._menu for page in item.pages]

    def create_navigation_layout(self):
        return dbc.NavbarSimple(
            [item.get_menu_item_layout() for item in self._menu],
            brand=self.title,
            color="primary",
            dark=True,
            sticky=True,
            className="mb-5",
        )

    def create_layout(self):
        return html.Div(
            children=[
                dcc.Location(id="url", refresh=False),
                self.create_navigation_layout(),
                dbc.Container(id="content", children=[], fluid=True),
            ]
        )

    def register_callbacks(self):
        """
        Implements generic callbacks common for all apps,
        here used for navigation

        Example:
        ```
            @self.callback(
                Output("nav", "children"), Input("nav-item", "value")
            )
            def common_nav_callback(nav_item_value):
                ...
                return nav_children
        ```
        """

        @self.callback(
            Output("content", "children"),
            [Input("url", "pathname")],
        )
        def display_page(pathname):
            for page in self.pages:
                if page.route.rstrip("/") == pathname.rstrip("/"):
                    return page.layout

            return html.Div(
                dbc.Container(
                    [
                        html.H2("Error 404!"),
                        html.P("Page not found."),
                    ],
                    fluid=True,
                    className="py-2 text-center",
                ),
                className="p-5 mx-4 bg-light",
            )

    def add_callbacks(self, callbacks: Callable[[Dash], None]):
        callbacks(self)
