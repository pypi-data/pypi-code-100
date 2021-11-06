import logging
from pathlib import Path

import html5lib
from html5lib.treewalkers import getTreeWalker

from ruteni import STATICNS, configuration

logger = logging.getLogger(__name__)

COMPONENTSNS = STATICNS.add("components")

dependencies: dict[str, set[str]] = {}


def load_component_dir(directory: Path) -> None:
    for node in directory.iterdir():
        if node.is_file():
            if node.suffix == ".js":
                configuration.add_file_route(node.name + ".js", node, ns=COMPONENTSNS)
            else:
                logger.warn(f"file {node} ignored")
        else:
            index_js = node.joinpath("index.js")
            if index_js.exists():
                configuration.add_file_route(
                    node.name + ".js", index_js, ns=COMPONENTSNS
                )

                index_html = node.joinpath("index.html")
                if index_html.exists():
                    with open(index_html, "rb") as f:
                        fragment = html5lib.parseFragment(f)
                    walker = getTreeWalker("etree")
                    stream = walker(fragment)
                    dependencies[node.name] = set()
                    for element in stream:
                        if element["type"] == "StartTag":
                            if "-" in element["name"]:
                                dependencies[node.name].add(element["name"])
                    configuration.add_file_route(
                        node.name + ".html", index_html, ns=COMPONENTSNS
                    )

                index_css = node.joinpath("index.css")
                if index_css.exists():
                    configuration.add_file_route(
                        node.name + ".css", index_css, ns=COMPONENTSNS
                    )
            else:
                logger.warn(f"missing index.js in '{node}'")


logger.info("loaded")
