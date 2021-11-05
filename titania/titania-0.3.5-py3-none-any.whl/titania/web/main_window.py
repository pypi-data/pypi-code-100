import inspect

from views.VELOView.ThresholdView.thresholds_web import ThresholdsWeb
import mpld3
from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import *

from titania.web.base_tab import BaseWebTabFactory


class MainWindow:

    def __init__(self, tab_config=None):
        self.nav = Nav()
        self.app = Flask(__name__, template_folder='template')
        self.subgroup_list = []
        self.widgets = tab_config
        self.tab_factory = BaseWebTabFactory()
        self.set_main_layout()

    def set_main_layout(self):
        self.set_methods_for_each_endpoint()
        self.add_endpoint('/', '/', handler=self.home)
        self.add_all_endpoints()
        self.set_navigation()

    def add_all_endpoints(self):
        for main_tab in self.widgets:
            list = []
            for widget in self.widgets[main_tab]:
                widget_object = widget()
                url = "/" + main_tab + "/" + widget_object.title
                list.append(View(widget_object.title, url))
                method_to_call = getattr(self.__class__, widget_object.title)
                self.add_endpoint(url, url, handler=method_to_call)

            self.subgroup_list.append(Subgroup(
                main_tab,
                *list
            ), )

    # TODO rethink creating widget every time it is called
    def set_methods_for_each_endpoint(self):
        for main_tab in self.widgets:
            for widget in self.widgets[main_tab]:
                widget_object = widget()
                self.tab_factory.build(self.__class__, widget_object)

    def set_navigation(self):
        self.nav.register_element('top', Navbar(
            View('Widgits, Inc.', ''),
            *self.subgroup_list
        ))

    def home(self):
        b = BaseWebTabFactory()
        html = b.build(self.__class__, ThresholdsWeb())
        return render_template('index.html', plot_dict=Markup(html))

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler)

    def run(self):
        self.nav.init_app(self.app)
        self.app.run()
