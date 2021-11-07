import os 
from os import getcwd, mkdir, path
import sys
import shutil
import time 
import importlib 
import re
import fileinput
from jinja2 import Template

TEMPLATE_PATH = os.getcwd()

# utils
def get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

def to_snake_case(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def model_reader(model_name, model_path):
    fields = []
    with open(model_path) as file:
        isFound = False
        lines = file.readlines()
        for line in lines :  
            line.replace("\n", "")  
            line = line.strip()
            if "class" in line and "class %s" % model_name not in line and isFound: 
                isFound = False   
            if "class %s" % model_name in line or (isFound and line != ""):
                if "class %s" % model_name not in line and "=" in line:
                    line_split = line.split("=")
                    if "db.Column" in line_split[1] :
                        fields.append(line_split[0].strip())
                isFound = True
    return fields

def _scaffold(template, target_path, **kwargs):
    with open(TEMPLATE_PATH.format(template), 'r') as f:
        template = Template(f.read())
    template.stream(**kwargs).dump(target_path)

def generate_detail(name, app_path, fields):
    path_ = path.join(app_path, 'templates/%s.html' % name)

    form = {}
    form["name"] = name
    form["main_field"] = fields[0]
    form["fields"] = fields
    _scaffold('template_detail.html', path_, _NAME_=name.capitalize(), _FORM_=form)

def generate_list(name, app_path, fields):
    path_ = path.join(app_path, 'templates/%s_list.html' % name)

    form = {}
    form["name"] = name
    form["main_field"] = fields[0]
    form["fields"] = fields
    _scaffold('template_list.html', path_, _NAME_=name.capitalize(), _FORM_=form)

def generate_form(name, app_path, fields):
    path_ = path.join(app_path, 'forms/%s.py' % name)

    form = {}
    form["name"] = name
    form["main_field"] = fields[0]
    form["fields"] = fields
    _scaffold('form.py', path_, _NAME_=name.capitalize(), _FORM_=form)

def generate_view(name, app_path, fields):
    path_ = path.join(app_path, 'views/%s.py' % name)

    form = {}
    form["name"] = name
    form["main_field"] = fields[0]
    form["fields"] = fields
    _scaffold('view.py', path_, _NAME_=name.capitalize(), _FORM_=form)

def update_init_view(name, app_path, fields):
    template_string  = """\n\n# import {{_NAME_}} Form & Model\nfrom ..forms.{{_FORM_.name}} import {{_NAME_}}Form\nfrom ..models.{{_FORM_.name}} import {{_NAME_}}"""
    outer_template = Template(template_string)

    path_ = path.join(app_path, 'views/__init__.py')

    form = {}
    form["name"] = name
    form["main_field"] = fields[0]
    form["fields"] = fields
    rendered_text = outer_template.render( 
        _NAME_=name.capitalize(), 
        _FORM_=form,
        Template=Template
    )
    with open(path_, "a") as init_file:
        init_file.write(rendered_text)

def update_init_app(name, app_path, fields):
    template_string  = """\n\n# Late import models, forms & views ({{_NAME_}})\nfrom app.models.{{_FORM_.name}} import {{_NAME_}}\nfrom app.views.{{_FORM_.name}} import *\nfrom app.forms.{{_FORM_.name}} import *"""
    outer_template = Template(template_string)

    path_ = path.join(app_path, '__init__.py')

    form = {}
    form["name"] = name
    form["main_field"] = fields[0]
    form["fields"] = fields
    rendered_text = outer_template.render( 
        _NAME_=name.capitalize(), 
        _FORM_=form,
        Template=Template
    )
    with open(path_, "a") as init_file:
        init_file.write(rendered_text)

def update_layout(name, app_path, fields):
    template_string  = """            
            <li class="nav-item">
                {{ '<a class="nav-link" href="{{ url_for(' ~ _FORM_.name_q ~ ')}}"><span class="fa fa-question-circle-o mr-1"></span>' ~ _NAME_ ~ '</a>' }}
            </li>
            <!-- NEW MENU HERE (DONT CHANGE/REMOVE THIS COMMENT) -->
            """
    outer_template = Template(template_string)

    path_ = path.join(app_path, 'templates/_layout.html')

    form = {}
    form["name"] = name
    form["name_q"] = "'" + name + "s'"
    form["main_field"] = fields[0]
    form["fields"] = fields
    rendered_text = outer_template.render( 
        _NAME_=name.capitalize(), 
        _FORM_=form,
        Template=Template
    )
    with fileinput.FileInput(path_, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("<!-- NEW MENU HERE (DONT CHANGE/REMOVE THIS COMMENT) -->", rendered_text), end='')

if __name__ == '__main__': 
    # read parameter 
    model_name = get(sys.argv, 1, default='') 
    model_path = get(sys.argv, 2, default=os.getcwd()) 
    if model_name == '':
        raise Exception("Can't find model name '%s' in path %s" % (model_name, model_path))
    if not os.path.exists(model_path) :
        raise Exception("Can't find model path  %s" % (model_path))
    if not os.path.isfile(model_path) :
        raise Exception("This path %s is not a python file where model %s located." % (model_path, model_name))

    print("\n[INFO] Prepare to create a new UI Flask Scaffoling Base with name %s" % (model_name))
    time.sleep(2)

    fields = model_reader(model_name, model_path)
    del fields[0]

    # create lis & detail template
    import scaffold
    pkgdir = sys.modules['scaffold'].__path__[0]
    source_path = os.path.join(pkgdir, 'stubs')
    TEMPLATE_PATH = path.join(source_path, '{}.jinja2')
    
    TARGET_TEMPLATE_PATH = os.path.dirname(os.path.dirname(model_path))
    generate_detail(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)
    generate_list(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)
    generate_form(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)
    generate_view(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)
    update_init_view(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)
    update_init_app(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)
    update_layout(to_snake_case(model_name), TARGET_TEMPLATE_PATH, fields)