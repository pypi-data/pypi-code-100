import math

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from repopip.local_repo.repo import Repo
from repopip.local_repo.configurator import Configurator
from repopip.translations.translator import Translator

repo = Repo()
translator = Translator()
translations = translator.translations
app_lang = 'en'

bp = Blueprint('site', __name__)

@bp.route('/')
@bp.route('/<lang>')
def index(lang = app_lang):
    if(lang not in translator.translations):
        lang = app_lang
    translation = {**translations[lang]['nav'], **translations[lang]['index'], **translations[lang]['footer']}
    
    return render_template('pages/index.html.j2', **translation, terminal = True)


@bp.route('/contact')
@bp.route('/<lang>/contact')
def contact(lang = app_lang):
    if(lang not in translator.translations):
        lang = app_lang
    translation = {**translations[lang]['nav'], **translations[lang]['contact'], **translations[lang]['footer']}
    return render_template('pages/contact.html.j2', **translation)


@bp.route('/packages')
@bp.route('/<lang>/packages')
def packages(lang = app_lang):
    if(lang not in translator.translations):
        lang = app_lang
    translation = {**translations[lang]['nav'], **translations[lang]['packages'], **translations[lang]['footer']}
    
    repo.loadPackages()
    packages = repo.packages
    repo_len = len(packages)
    total = (repo_len, repo.total_versions)

    if(request.args.get('all')):
        return render_template('pages/packages.html.j2', **translation, packages_dict = packages, total = total, size = repo.size)

    page = request.args.get('page')
    if(page is not None and page.isnumeric()):
         page = int(page)
    else:
        page = 1

    step = 12
    total_pages = math.ceil(repo_len/step)
    start = page * step - step
    end = start + step
    slice_packages = dict(list(packages.items())[start:end])
    data_pages = {
        'current': page,
        'total_pages':  total_pages
    }
    return render_template('pages/packages.html.j2', **translation, packages_dict = slice_packages, total = total, size = repo.size, data_pages = data_pages)


@bp.route('/config', methods=['GET', 'POST'])
@bp.route('/<lang>/config', methods=['GET', 'POST'])
def configuration(lang = app_lang):
    if(lang not in translator.translations):
        lang = app_lang
    translation = {**translations[lang]['nav'], **translations[lang]['configuration'], **translations[lang]['footer']}

    if(request.method == "POST"):
        try:
            if(request.json.get('config') == 'standar'):
                c = Configurator(request.json.get('level'))
            else:
                c = Configurator(request.json.get('level'), request.json.get('config'))

            c.config()
            return { 'result':True }
        except:
            return { 'result':False }
    else:
        configs = Configurator().searchConfigs()        

        return render_template('pages/configuracion.html.j2', **translation, configs = configs)

@bp.route('/get-configs', methods=['GET', 'POST'])
def getConfigs():
    try:
        configs = Configurator().searchConfigs()
        return { 'error': False, 'configs': configs }
    except Exception:
        return { 'error' : True }