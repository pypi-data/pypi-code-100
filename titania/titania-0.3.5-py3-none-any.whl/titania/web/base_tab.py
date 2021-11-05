import inspect

import mpld3
from flask import render_template
from markupsafe import Markup



class BaseTab:
    pass




class BaseWebTabFactory:
    def build(self, cls,widget_object):
        def innerdynamo():
            widget_object.initiate_for_web()
            if widget_object.plot is not None:
                html = mpld3.fig_to_html(widget_object.plot.figure)
            else:
                html = ""
            return render_template('index.html', plot_dict=Markup(html))

        innerdynamo.__name__ = widget_object.title
        setattr(cls, innerdynamo.__name__, innerdynamo)
