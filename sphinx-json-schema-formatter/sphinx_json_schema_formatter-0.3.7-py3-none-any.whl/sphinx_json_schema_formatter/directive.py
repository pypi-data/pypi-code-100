import os.path
from functools import cached_property
from typing import List, Dict, Any, Optional

import docutils.parsers.rst
import docutils.utils
import docutils.frontend
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from sphinx.directives.code import container_wrapper

from .loader import JsonSchemaLoader


def parse_rst(text: str) -> nodes.document:
    parser = docutils.parsers.rst.Parser()
    components = (docutils.parsers.rst.Parser,)
    settings = docutils.frontend.OptionParser(
        components=components
    ).get_default_values()
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document


class JsonSchema(Directive):
    optional_arguments = 1
    has_content = True

    def get_file_or_url(self) -> Optional[str]:
        if len(self.arguments) == 0:
            return None
        file_or_url = self.arguments[0]
        if file_or_url.startswith("http"):
            return file_or_url
        if os.path.isabs(file_or_url):
            return file_or_url
        # file relative to the path of the current rst file
        dname = os.path.dirname(self.state_machine.input_lines.source(0))
        path = os.path.join(dname, file_or_url)
        if os.path.exists(path):
            return path
        root_dir = self.state.document.settings.env.config.json_schema_root_dir
        if root_dir is None:
            return None
        # no file at relative location, try loading from root directory
        file_or_url = os.path.join(root_dir, file_or_url)
        if not os.path.exists(file_or_url):
            return None
        return file_or_url

    @cached_property
    def schema(self) -> Optional[Dict[str, Any]]:
        file_or_url = self.get_file_or_url()
        if file_or_url:
            jsonschema = JsonSchemaLoader(file_or_url)
            return jsonschema.schema
        elif self.content:
            jsonschema = JsonSchemaLoader(
                self.content, self.state_machine.input_lines.source(0)
            )
            return jsonschema.schema
        else:
            return None

    @cached_property
    def required_properties(self) -> List[str]:
        if self.schema is None:
            return []
        return self.schema.get("required", [])

    @cached_property
    def jsonschema_content(self) -> List[nodes.section]:
        return []

    def handle_property(self, title, prop) -> None:
        section = nodes.section(ids=[title], names=[title])
        titlenode = nodes.title(title, title)
        section += titlenode
        description = prop.get("description", "")
        desc_view = ViewList(description.split("\n"))
        desc = nodes.description()
        self.state.nested_parse(desc_view, self.content_offset, desc)
        section += desc
        is_required = title in self.required_properties
        required = nodes.description()
        required_label = nodes.strong(text="Required: ")
        required_text = nodes.inline(text=f"{is_required}")
        required += required_label
        required += required_text
        section += required
        default_value = prop.get("default")
        if default_value:
            default = nodes.description()
            default_label = nodes.strong(text="Default: ")
            default_text = nodes.inline(text=f"{default_value}")
            default += default_label
            default += default_text
            section += default
        self.jsonschema_content.append(section)

    def run(self):
        if self.schema is None:
            return []
        properties = self.schema.get("properties", {})
        sorted_props = {k: properties[k] for k in sorted(properties)}
        for title, prop in sorted_props.items():
            self.handle_property(title, prop)
        return self.jsonschema_content
