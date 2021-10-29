import os
import pytest

from magnumapi.tool_adapters.ToolAdapterFactory import ToolAdapterFactory
from magnumapi.tool_adapters.roxie.RoxieToolAdapter import TerminalRoxieToolAdapter
from magnumapi.tool_adapters.roxie.RoxieToolAdapter import DockerTerminalRoxieToolAdapter
from tests.resource_files import create_resources_file_path


def test_init_with_json_terminal_roxie():
    # arrange
    config_path = create_resources_file_path('resources/tool_adapters/roxie/terminal_roxie.json')

    # act
    tool_adapter = ToolAdapterFactory.init_with_json(config_path)

    # assert
    assert isinstance(tool_adapter, TerminalRoxieToolAdapter)
    assert 'input' == tool_adapter.input_folder_rel_path
    assert 'runroxie' == tool_adapter.executable_name
    assert 'input%sroxieData.xml' % os.sep == tool_adapter.xml_output_file_path
    assert 'input%sinput.output' % os.sep == tool_adapter.output_file_path
    assert 'input%sinput.data' % os.sep == tool_adapter.input_file_path
    assert 'input%sroxieold_2.cadata' % os.sep == tool_adapter.cadata_file_path
    assert 'roxieold_2.cadata' == tool_adapter.cadata_file


def test_init_with_json_docker_terminal_roxie():
    # arrange
    config_path = create_resources_file_path('resources/tool_adapters/roxie/docker_terminal_roxie.json')

    # act
    tool_adapter = ToolAdapterFactory.init_with_json(config_path)

    # assert
    assert isinstance(tool_adapter, DockerTerminalRoxieToolAdapter)
    assert 'input' == tool_adapter.input_folder_rel_path
    assert 'runroxie' == tool_adapter.executable_name
    assert 'input%sroxieData.xml' % os.sep == tool_adapter.xml_output_file_path
    assert 'input%sinput.output' % os.sep == tool_adapter.output_file_path
    assert 'input%sinput.data' % os.sep == tool_adapter.input_file_path
    assert 'input%sroxieold_2.cadata' % os.sep == tool_adapter.cadata_file_path
    assert 'runroxie' == tool_adapter.executable_name
    assert 'roxieold_2.cadata' == tool_adapter.cadata_file


def test_init_with_dict_terminal_roxie():
    # arrange
    config = {
        "executable_name": "runroxie",
        "input_folder_rel_path": "input",
        "input_file": "input.data",
        "output_file": "input.output",
        "cadata_file": "roxieold_2.cadata",
        "xml_output_file": "roxieData.xml"
    }

    # act
    tool_adapter = ToolAdapterFactory.init_with_dict(config)

    # assert
    assert isinstance(tool_adapter, TerminalRoxieToolAdapter)
    assert 'input' == tool_adapter.input_folder_rel_path
    assert 'runroxie' == tool_adapter.executable_name
    assert 'input%sroxieData.xml' % os.sep == tool_adapter.xml_output_file_path
    assert 'input%sinput.output' % os.sep == tool_adapter.output_file_path
    assert 'input%sinput.data' % os.sep == tool_adapter.input_file_path
    assert 'input%sroxieold_2.cadata' % os.sep == tool_adapter.cadata_file_path
    assert 'roxieold_2.cadata' == tool_adapter.cadata_file


def test_init_with_dict_docker_terminal_roxie():
    # arrange
    config = {
        "executable_name": "runroxie",
        "input_folder_rel_path": "input",
        "input_file": "input.data",
        "output_file": "input.output",
        "cadata_file": "roxieold_2.cadata",
        "xml_output_file": "roxieData.xml",
        "docker_image_name": "roxie_terminal"
    }

    # act
    tool_adapter = ToolAdapterFactory.init_with_dict(config)

    # assert
    assert isinstance(tool_adapter, DockerTerminalRoxieToolAdapter)
    assert 'input' == tool_adapter.input_folder_rel_path
    assert 'runroxie' == tool_adapter.executable_name
    assert 'input%sroxieData.xml' % os.sep == tool_adapter.xml_output_file_path
    assert 'input%sinput.output' % os.sep == tool_adapter.output_file_path
    assert 'input%sinput.data' % os.sep == tool_adapter.input_file_path
    assert 'input%sroxieold_2.cadata' % os.sep == tool_adapter.cadata_file_path
    assert 'roxieold_2.cadata' == tool_adapter.cadata_file


def test_init_with_dict_docker_terminal_roxie_error():
    # arrange
    config = {
        "executable_name": "runroxie",
        "input_folder_rel_path": "input",
        "input_file": "input.data",
        "output_file": "input.output",
        "cadata_file": "roxieold_2.cadata",
        "xml_output_file": "roxieData.xml",
        "docker_image": "roxie_terminal"
    }

    # act
    with pytest.raises(KeyError) as exc_info:
        tool_adapter = ToolAdapterFactory.init_with_dict(config)

    assert 'The input config definition keys dict_keys([\'executable_name\', \'input_folder_rel_path\', ' \
           '\'input_file\', \'output_file\', \'cadata_file\', \'xml_output_file\', \'docker_image\']) ' \
           'do not match any tool adapter constructor signature!' in str(exc_info.value)
