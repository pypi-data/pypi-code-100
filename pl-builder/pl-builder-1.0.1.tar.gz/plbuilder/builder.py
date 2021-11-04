from pathlib import Path
from typing import Sequence, List, Optional, Union
import importlib.util
import os
import sys

from pydantic import BaseModel
from pyexlatex.logic.output.api.formats import OutputFormats
from pyexlatex.models.document import DocumentBase

from plbuilder.paths import (
    SLIDES_SOURCE_PATH,
    slides_source_path,
    DOCUMENTS_SOURCE_PATH,
    documents_source_path,
    templates_path_func,
)
from plbuilder.templater import output_template

sys.path.append(
    os.path.abspath(os.getcwd())
)  # needed to be able to import local plbuild directory

IGNORED_FILES = [
    "__init__.py",
]


class BuildOptions(BaseModel):
    output_folder: Path
    file_name: str
    output_format: OutputFormats = OutputFormats.PDF
    handouts_folder: Optional[Path] = None


class BuildConfig(BaseModel):
    model: DocumentBase
    options: BuildOptions

    class Config:
        arbitrary_types_allowed = True


def get_all_source_files() -> List[str]:

    slide_sources = [
        file
        for file in next(os.walk(SLIDES_SOURCE_PATH))[2]
        if file not in IGNORED_FILES
    ]
    slide_sources = [slides_source_path(file) for file in slide_sources]
    doc_sources = [
        file
        for file in next(os.walk(DOCUMENTS_SOURCE_PATH))[2]
        if file not in IGNORED_FILES
    ]
    doc_sources = [documents_source_path(file) for file in doc_sources]
    return slide_sources + doc_sources


def build_all(desired_output_format: Optional[OutputFormats] = None):
    files = get_all_source_files()
    [
        build_by_file_path(file, desired_output_format=desired_output_format)
        for file in files
    ]


def build_by_file_path(
    file_path: str, desired_output_format: Optional[OutputFormats] = None
):
    _print_now(f"Building {file_path}")
    mod = _module_from_file(file_path)

    configs: List[BuildConfig] = mod.get_outputs()  # type: ignore
    for config in configs:
        if desired_output_format is not None:
            # Override file setting if user passes setting in CLI
            config.options.output_format = desired_output_format
        _build_by_config(config)
        _print_now(f"Done creating {config.options.file_name}.")


def _build_by_config(config: BuildConfig):
    if not os.path.exists(config.options.output_folder):
        os.makedirs(config.options.output_folder)

    _output_document(
        config.model,
        str(config.options.output_folder),
        config.options.file_name,
        output_format=config.options.output_format,
    )


def _output_document(
    doc: DocumentBase,
    outfolder: str,
    out_name: str,
    output_format: OutputFormats = OutputFormats.PDF,
):
    if output_format == OutputFormats.PDF:
        out_method = getattr(doc, "to_pdf")
    elif output_format == OutputFormats.HTML:
        out_method = getattr(doc, "to_html")
    else:
        raise ValueError(f"unsupported output format {output_format}")

    out_method(outfolder, out_name)


def _module_from_file(file_path: str):
    mod_name = os.path.basename(file_path).strip(".py")
    return _module_from_file_and_name(file_path, mod_name)


def _module_from_file_and_name(file_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ValueError(f"could not extract spec from {file_path} {module_name}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def _print_now(*args):
    print(*args)
    sys.stdout.flush()


if __name__ == "__main__":
    build_all()
