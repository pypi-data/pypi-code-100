from flask import Flask
from mitre_attack.data.matrices.enterprise import MitreAttackEnterprise

import mitre_attack.cli.click as click
import logging
import flask
import sys


logger = logging.getLogger(__name__)

app = Flask(__name__)
api = MitreAttackEnterprise()


@app.route('/tactics')
def tactics():
    response = list(api.iter_tactics())
    return flask.jsonify(response)


@app.route('/techniques')
def techniques():
    technique_ids = flask.request.args.getlist('technique_ids')
    technique_names = flask.request.args.getlist('technique_names')
    limit = int(flask.request.args.get('limit', 0)) or None

    response = list(api.iter_techniques(technique_ids=technique_ids, technique_names=technique_names, limit=limit))
    return flask.jsonify(len(response))


@app.route('/groups')
def groups():
    response = list(api.iter_groups(limit=limit))
    return flask.jsonify(response)


@app.route('/software')
def software():
    response = list(api.iter_software())
    return flask.jsonify(response)


@app.route('/malware')
def malware():
    response = list(api.iter_malware_families())
    return flask.jsonify(response)


@app.route('/tools')
def tools():
    response = list(api.iter_tools())
    return flask.jsonify(response)


@app.route('/relationships')
def relationships():
    response = list(api.iter_relationships())
    return flask.jsonify(response)


@click.command()
def cli():
    app.run()


if __name__ == "__main__":
    cli()
