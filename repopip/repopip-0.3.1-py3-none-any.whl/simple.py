import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, send_from_directory
)

from repopip.local_repo import SIMPLE_PATH, repo

repo = repo.Repo()

bp = Blueprint('simple', __name__, url_prefix='/')

@bp.route('/simple/')
def simple():
    repo.loadPackages()
    return render_template('simple/simple.html.j2', packages=repo.packages.keys())


@bp.route('/simple/<package>')
def get_package(package):
    return send_from_directory(SIMPLE_PATH, package)


@bp.route('/simple/<pakage>/')
def pakage(pakage):
    return render_template('simple/pakage.html.j2', packages=repo.getPackage(pakage))