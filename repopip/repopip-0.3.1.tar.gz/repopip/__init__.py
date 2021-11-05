from flask import Flask, render_template, send_from_directory, session
import os

from repopip.util import filesize, url
from repopip import site, simple
from repopip.local_repo.repo import Repo

repo = Repo()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'repopip.sqlite'),
    )

    app.add_template_filter(filesize)
    app.add_template_filter(url)

    app.register_blueprint(site.bp)
    app.register_blueprint(simple.bp)

    return app

