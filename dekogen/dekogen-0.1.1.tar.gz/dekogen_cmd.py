"""Command line util based on click"""
import click
from dekogen.spec_codegen import PythonResponsesGenerator, PythonRequestsGenerator
from dekogen.spec_reader import SpecReader


class Session:
    """Stores base session data"""
    py_resp_gen = PythonResponsesGenerator
    py_req_gen = PythonRequestsGenerator
    spec_reader = SpecReader


# TODO: Upload into pip

@click.group(invoke_without_command=True)
@click.pass_context
def run(context):
    """Entry point"""


@run.command()
@click.option("-f", "--file", help=u"Use local file path", default=False)
@click.option("-l", "--link", help=u"Use file link", default=False)
@click.option("-o", "--output", help=u"Output path for generated file", default='')
@click.option("-t", "--spec-format", help=u"Specification file type (yaml, json etc.) ", default='yaml')
@click.pass_context
def generate_responses_python(context, file, link, output, spec_format):
    """Generate responses .py file according to provided data"""
    if spec_format.lower() != 'yaml':
        raise click.exceptions.UsageError('Not supported specs format: {0}'.format(spec_format.lower()), context)
    spec_reader = context.obj.spec_reader
    spec_data = spec_reader.read_yaml(link=link, file_path=file)
    py_resp_generator = context.obj.py_resp_gen(spec_data, output)
    py_resp_generator.generate()
    click.echo("File stored in {0}".format(output))


@run.command()
@click.option("-f", "--file", help=u"Use local file path", default=False)
@click.option("-l", "--link", help=u"Use file link", default=False)
@click.option("-o", "--output", help=u"Output path for generated file", default='')
@click.option("-t", "--spec-format", help=u"Specification file type (yaml, json etc.) ", default='yaml')
@click.pass_context
def generate_requests_python(context, file, link, output, spec_format):
    """Generate requests .py file according to provided data"""
    if spec_format.lower() != 'yaml':
        raise click.exceptions.UsageError('Not supported specs format: {0}'.format(spec_format.lower()), context)
    spec_reader = context.obj.spec_reader
    spec_data = spec_reader.read_yaml(link=link, file_path=file)
    py_req_generator = context.obj.py_req_gen(spec_data, output)
    py_req_generator.generate()
    click.echo("File stored in {0}".format(output))


@run.command()
@click.option("-f", "--file", help=u"Use local file path", default=False)
@click.option("-l", "--link", help=u"Use file link", default=False)
@click.option("-o", "--output", help=u"Output path for generated file", default='')
@click.option("-t", "--spec-format", help=u"Specification file type (yaml, json etc.) ", default='yaml')
@click.pass_context
def generate_all_python(context, file, link, output, spec_format):
    """Generate responses and requests .py files according to provided data"""
    if spec_format.lower() != 'yaml':
        raise click.exceptions.UsageError('Not supported specs format: {0}'.format(spec_format.lower()), context)
    spec_reader = context.obj.spec_reader
    spec_data = spec_reader.read_yaml(link=link, file_path=file)
    py_resp_generator = context.obj.py_resp_gen(spec_data, output)
    py_resp_generator.generate()
    click.echo("Responses file stored in {0}".format(output))
    py_req_generator = context.obj.py_req_gen(spec_data, output)
    py_req_generator.generate()
    click.echo("Requests file stored in {0}".format(output))


run.add_command(generate_requests_python)
run.add_command(generate_responses_python)
run.add_command(generate_all_python)

run(
        obj=Session(),
        help_option_names=["-h", "--help"],
        max_content_width=120,
)
