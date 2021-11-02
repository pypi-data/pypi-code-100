import json
import os
import sys

import yaml
from jinja2 import Template

from mesiqi.core import connector_factory, connector_loader, jobfactory
from mesiqi.core.jobfactory import JobFactory
from mesiqi.core.logger import get_logger
from mesiqi.core.utils import get_env


logger = get_logger(__name__)


def run_all_job_in_directory(path: str = "./jobs"):

    full_path = os.path.join(os.getcwd(), path)
    if not os.path.exists(full_path):
        logger.info(f"path not found: {full_path}")
        return full_path  #'FAILED'

    jobs = [
        os.path.join(d, x)
        for d, dirs, files in os.walk(path)
        for x in files
        if x.endswith(".yml")
    ]

    for job in jobs:
        ret = run_job(job)
        if ret != "DONE":
            logger.info(f"Error running job: {job}")

    return "DONE"


def run_job(source: str):

    with open(source, "r") as stream:
        try:
            jobs_spec = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            logger.info(f"Error loading jobs.yml: {exception}")

        # Replace 'env_var' in template 
        jobs_config = json.loads(
            Template(json.dumps(jobs_spec)).render(env_var=get_env), strict=False
        )["jobs"]

        # Load plugins for source og target
        source_types = [job["source"]["type"] for job in jobs_config]
        sink_types = [job["target"]["type"] for job in jobs_config]
        types = list(set(source_types + sink_types))
        connector_loader.load_plugins(types)

        # Run E(T)L jobs
        for job_config in jobs_config:
            start_time = time.time()
            logger.info(f"Starting job: {job_config['source'].get('name', None)} - {job_config['target'].get('name', None)}")
            source_connector = connector_factory.create(job_config["source"])
            sink_connector = connector_factory.create(job_config["target"])
            job = JobFactory(source_connector, sink_connector, job_config["config"])()
            job.run()
            duration = round(time.time() - start_time,2)
            logger.info(f"Job completed in {duration} seconds")

    return "DONE"
