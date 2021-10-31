from bokeh.models.annotations import Legend
from flask import Flask, render_template, request, send_from_directory
from flask_cors import CORS

from bokeh.plotting import figure 
from bokeh.embed import json_item
from bokeh.palettes import Category20_20
import bokeh.resources

import numpy as np
import json
import yaml
import click
import shutil as sh

import os
from os.path import dirname, basename, realpath, join

from .models import Project, Folder, Experiment, init_db
from .utils import APISuccess, APIError, update
from xpipe.config import load_config_from_str, to_dict

from mongoengine import base, connect
import signal
from multiprocessing import Process

dir_path = dirname(realpath(__file__))

@click.command()
@click.option("--host", default="127.0.0.1", help="Flask host")
@click.option("--port", default="5000", help="Flask port")
@click.option("--db-host", default="127.0.0.1", help="IP Address of the MongoDB server")
@click.option("--db-port", default=27017, help="Port of the MongoDB server")
@click.option("--artifacts-dir", default="./artifacts", help="Folder to store artifacts")
def run(host, port, db_host, db_port, artifacts_dir):
    connect("xpipe", host=db_host, port=db_port) # Connect to mongodb
    init_db() # Initialize models

    artifacts_dir = os.path.join(os.getcwd(), artifacts_dir)
    static_dir = os.path.join(dir_path, "frontend/build")
    app = Flask(__name__, 
        static_url_path="/", 
        static_folder=static_dir,
        template_folder=static_dir)
    CORS(app)
    prepare_bokeh_dependancies() # Copy bokeh js dependancies into ./frontend/public

    print("""
     ██╗  ██╗██████╗ ██╗██████╗ ███████╗
     ╚██╗██╔╝██╔══██╗██║██╔══██╗██╔════╝
      ╚███╔╝ ██████╔╝██║██████╔╝█████╗  
      ██╔██╗ ██╔═══╝ ██║██╔═══╝ ██╔══╝  
     ██╔╝ ██╗██║     ██║██║     ███████╗
     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝""")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/explorer")
    @app.route("/explorer/<path:path>")
    @app.route("/experiment")
    @app.route("/experiment/<path:path>")
    def xpipe(path=None):
        return render_template("index.html")
    
    @app.route('/artifacts/<path:filename>')
    def base_static(filename):
        return send_from_directory(artifacts_dir, filename)

    # Backend API

    @app.route("/api/folder/new", methods=["POST", "GET"])
    def create_folder():
        data = request.json
        path = data["folder"]
        parent_dir = dirname(path)

        if Folder.exists(parent_dir) and not Folder.exists(path):
            folder = Folder.get_folder(parent_dir)
            new_folder = Folder()
            new_folder.name = basename(path)
            new_folder.parent_folder = folder.pk
            new_folder.save()
            folder.update(push__children_folders=new_folder.pk)
            
            return APISuccess({
                "message": f"Folder {request.json['folder']} successfully created"
            }).json()
        return APIError("Can't create new folder").json()

    @app.route("/api/folder/params_metrics", methods=["POST", "GET"])
    def folder_params():
        data = request.json
        folder = Folder.get_folder(data["folder"])
        exps = Experiment.objects(parent_folder=folder.pk)
        confs = [exp.to_mongo()["configuration"] for exp in exps]
        metrics = [exp.list_metrics() for exp in exps]
        metrics = set().union(*metrics)
        if len(confs) == 0:
            return APISuccess({"params": {}}).json()
        conf = confs[0]
        for c in confs[1:]:
            conf = update(conf, c)
        return APISuccess({
            "params": conf,
            "metrics": list(metrics)
        }).json()

    @app.route("/api/folder/rename", methods=["POST"])
    def rename_folder():
        try:
            data = request.json
            folder = Folder.get_folder(data["folder"])
            folder.rename(data["new_name"])
            return APISuccess().json()
        except Exception as e:
            return APIError(f"Can't rename folder ({str(e)})").json()

    @app.route("/api/folder/delete", methods=["POST"])
    def delete_folder():
        data = request.json
        folder = Folder.get_folder(data["folder"]).delete()
        return APISuccess().json()

    @app.route("/api/folder/list", methods=["POST"])
    def list_folders():
        data = request.json
        parent_folder = Folder.get_folder(data["folder"])

        folders = parent_folder.children_folders
        sorted_indices = np.argsort([f.name for f in folders])
        folders = np.array([{"name": folder.name, "description": folder.description if folder.description is not None else ""} for folder in folders])
        folders = list(folders[sorted_indices])

        return APISuccess({
            "folders": folders
        }).json()

    @app.route("/api/run/list", methods=["POST"])
    def list_runs():
        data = request.json
        experiments = Experiment.list(data["folder"], order_by="start_date")
        experiments = [
            {
                **{"id": str(e.pk), "name": e.name},
                **{"params": {param_name: e.get_param(param_name) for param_name in data["params"]}},
                **{"metrics": {metric_name: e.get_metric(metric_name) for metric_name in data["metrics"]}},
                **{"commit_hash": e.commit_hash}, 
                **{"start_date": e.start_date_str}
            } for e in experiments
        ]
        return APISuccess({
            "experiments": experiments
        }).json()

    
    # Handle experiment labels
    # ----------------------------------------
    @app.route("/api/run/label/add", methods=["GET", "POST"])
    def add_label_to_exp():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            exp.add_label(data["label"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/label/delete", methods=["GET", "POST"])
    def delete_label_of_exp():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            exp.delete_label(data["label"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()
    
    @app.route("/api/run/label/list", methods=["GET", "POST"])
    def list_labels_of_exp():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            return APISuccess({
                "labels": exp.labels
            }).json()
        except Exception as e:
            return APIError(str(e)).json()
    # ----------------------------------------
    # Handle experiment notes
    # ----------------------------------------
    @app.route("/api/run/notes/get", methods=["GET", "POST"])
    def get_exp_notes():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            return APISuccess({"notes": exp.notes}).json()
        except Exception as e: 
            return APIError(str(e)).json()

    @app.route("/api/run/notes/set", methods=["GET", "POST"])
    def set_exp_notes():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            exp.update(set__notes=data["notes"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()
    # ----------------------------------------
    # Draw metric
    # ----------------------------------------
    @app.route("/api/run/graph", methods=["GET", "POST"])
    def draw_graph():
        try: 
            data = request.json
            exp = Experiment.get(data["id"])
            y = exp.get_timeserie(data["metric"]).y
            x = [i for i in range(len(y))]
            p = figure(sizing_mode='stretch_both', title=data["metric"])
            p.line(x, y)
            return APISuccess({"graph": json_item(p)}).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/compare/graph", methods=["GET", "POST"])
    def draw_compare_graph():
        
        try: 
            data = request.json
            exps = [Experiment.get(i) for i in data["ids"]]

            p = figure(sizing_mode='stretch_both', title=data["metric"])
            plotted_exps = []
            for i, exp in enumerate(exps):
                timeserie = exp.get_timeserie(data["metric"])
                if timeserie is None:
                    continue
                y = timeserie.y
                x = [i for i in range(len(y))]

                # Check if exp name already exists and add (n) if needed
                name = exp.name
                if name in plotted_exps:
                    i = 1
                    while name + f" ({i})" in plotted_exps:
                        i += 1
                    name = name + f" ({i})"
                plotted_exps += [name]

                p.line(x, y, line_color=Category20_20[i], legend_label=name)

            p.legend.click_policy="hide"

            return APISuccess({"graph": json_item(p)}).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/metric/list", methods=["GET", "POST"])
    def list_metrics():
        try: 
            data = request.json
            exp = Experiment.get(data["id"])
            return APISuccess({"metrics": exp.list_metrics()}).json()
        except Exception as e: 
            return APIError(str(e)).json()

    @app.route("/api/compare/metric/list", methods=["GET", "POST"])
    def list_compare_metrics():
        try: 
            data = request.json
            exps = [Experiment.get(i) for i in data["ids"]]
            metrics = []
            for exp in exps:
                metrics += exp.list_metrics()
            metrics = list(set(metrics))
            print(metrics)
            return APISuccess({"metrics": metrics}).json()
        except Exception as e: 
            return APIError(str(e)).json()
    # ----------------------------------------

    # Backend API for python library
    @app.route("/api/check", methods=["GET", "POST"])
    def check():
        return APISuccess().json()

    @app.route("/api/run/new", methods=["GET", "POST"])
    def new_run():
        try:
            data = request.json
            name = data["name"]
            folder = data["folder"]
            exp = Experiment.new(
                folder, 
                name, 
                commit_hash=(data["commit_hash"] if "commit_hash" in data else "")
            )
            return APISuccess({"id": str(exp.pk)}).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/move", methods=["GET", "POST"])
    def move_run():
        data = request.json
        try:
            ids = data["ids"]
            new_folder = data["folder"]
            if not isinstance(ids, list):
                ids = [ids]
            
            for exp_id in ids:
                Experiment.get(exp_id).move(new_folder)
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/delete", methods=["GET", "POST"])
    def delete_run():
        data = request.json
        try:
            ids = data["ids"]
            if not isinstance(ids, list):
                ids = [ids]
            
            for exp_id in ids:
                Experiment.get(exp_id).delete()
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/get", methods=["GET", "POST"])
    def get_run():
        data = request.json
        try:
            exp = Experiment.get(data["id"])

            return APISuccess({
                "name": exp.name,
                "configuration": exp.to_mongo()["configuration"],
                "metrics": exp.get_metrics(), 
                "path": exp.parent_folder.get_full_path(), 
                "commit_hash": exp.commit_hash,
                "start_date": exp.start_date_str
            }).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/log_param", methods=["GET", "POST"])
    def log_param():
        try: 
            data = json.load(request.json)
            exp_id = data["id"]
            exp = Experiment.get(exp_id)

            if "params_file" not in data:
                raise Exception("No file provided.")

            parsed_file = load_config_from_str(data["params_file"])
            params_dict = to_dict(parsed_file)
            exp.update(set__configuration=params_dict)
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/log_metric", methods=["GET", "POST"])
    def log_metric():
        try:
            data = request.json
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            name, value = data["metric_name"], data["metric_value"]
            exp.log_metric(name, value)
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()
        
    @app.route("/api/run/log_artifact", methods=["GET", "POST"])
    def log_artifact():
        try:
            data = json.load(request.files["json"])
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            if exp is None:
                raise ValueError("Experiment not found")
            if "file" not in request.files:
                raise ValueError("No file to save")
                
            exp.log_artifact(request.files["file"], artifacts_folder=artifacts_dir)
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/list_artifacts", methods=["GET", "POST"])
    def list_artifacts():
        try: 
            data = request.json
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            return APISuccess({
                "artifacts": exp.list_artifacts(artifacts_folder=artifacts_dir)
            }).json()
        except Exception as e:
            return APIError(str(e)).json()
        
    @app.route("/api/run/log_graph", methods=["GET", "POST"])
    def log_graph():
        try:
            data = request.json
            exp_id = data["id"]
            name = data["name"]
            graph = data["graph"]
            exp = Experiment.get(exp_id)
            if exp is None:
                raise ValueError("Experiment not found")
                
            exp.log_graph(name, graph, artifacts_folder=artifacts_dir)
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/list_graphs", methods=["GET", "POST"])
    def list_graphs():
        try: 
            data = request.json
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            return APISuccess({
                "graphs": exp.list_graphs(artifacts_folder=artifacts_dir)
            }).json()
        except Exception as e:
            return APIError(str(e)).json()

    server = Process(target=app.run, kwargs={"host": host, "port": port, "debug": True})
    def stop_server(*args, **kwargs):
        server.terminate()

    signal.signal(signal.SIGINT, stop_server)
    server.start()
    server.join()

def prepare_bokeh_dependancies():
    try:
        print("Loading Bokeh javascript dependancies.")
        base_dir = bokeh.resources.INLINE.base_dir
        sh.copyfile(join(base_dir, "js/bokeh.min.js"), join(dir_path, "frontend/public/bokeh.min.js"))
        sh.copyfile(join(base_dir, "js/bokeh-widgets.min.js"), join(dir_path, "frontend/public/bokeh-widgets.min.js"))
        sh.copyfile(join(base_dir, "js/bokeh-tables.min.js"), join(dir_path, "frontend/public/bokeh-tables.min.js"))
        sh.copyfile(join(base_dir, "js/bokeh-api.min.js"), join(dir_path, "frontend/public/bokeh-api.min.js"))
    except:
        raise Exception("Can't load Bokeh javascript dependancies.")

run()