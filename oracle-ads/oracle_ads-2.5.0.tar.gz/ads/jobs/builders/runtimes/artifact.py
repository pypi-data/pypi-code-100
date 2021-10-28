#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/
import os
import shutil
import tempfile

import fsspec
import nbformat
from nbconvert import PythonExporter, preprocessors
from traitlets.config import Config


class Artifact:
    """Represents a OCI Data Science Job artifact.
    The Artifact class is designed to add an additional processing step on runtime/source code.
    before uploading it as data science job artifact.

    A sub-class should implement the build() method to do the additional processing.
    A sub-class is designed to be used with context manager so that the temporary files are cleaned up properly.

    For example, the NotebookArtifact implements the build() method to convert the notebook to python script.
    with NotebookArtifact(runtime) as artifact:
        # The build() method will be called when entering the context manager
        # The final artifact for the job will be stored in artifact.path
        upload_artifact(artifact.path)
        # Files are cleaned up when exit or if there is an exception.

    """

    def __init__(self, source, runtime=None) -> None:
        self.source = source
        self.path = None
        self.temp_dir = None
        self.runtime = runtime

    def __str__(self) -> str:
        if self.path:
            return self.path
        return self.source

    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.build()
        return self

    def __exit__(self, *exc):
        if self.temp_dir:
            self.temp_dir.cleanup()

    def build(self):
        """Builds the runtime artifact in the temporary directory.
        Subclass should implement this method to:
        1. Process the runtime
        2. Set the self.path to the final artifact path

        Raises
        ------
        NotImplementedError
            When this method is not implemented in the subclass.
        """
        raise NotImplementedError()


class NotebookArtifact(Artifact):
    """Represents a NotebookRuntime job artifact"""

    def __init__(self, source, runtime) -> None:
        super().__init__(source, runtime=runtime)

    def build(self):
        """Prepares job artifact for notebook runtime"""
        self.path = os.path.join(
            self.temp_dir.name,
            str(os.path.basename(self.source)).replace(".ipynb", ".py"),
        )
        with fsspec.open(self.source) as f:
            nb = nbformat.reads(f.read(), nbformat.NO_CONVERT)

        exporter = PythonExporter()

        if self.runtime != None and self.runtime.exclude_tag:
            c = Config()
            c.TagRemovePreprocessor.remove_cell_tags = self.runtime.exclude_tag
            trp = preprocessors.TagRemovePreprocessor(config=c)
            trp.preprocess(nb=nb, resources=None)
        source, _ = exporter.from_notebook_node(nb)

        with open(self.path, "wb") as f:
            f.write(source.encode("utf-8"))


class ScriptArtifact(Artifact):
    """Represents a ScriptRuntime job artifact"""

    def build(self):
        """Prepares job artifact for script runtime.
        If the source is a file, it will be returned as is.
        If the source is a directory, it will be compressed as a zip file.
        """
        source = os.path.abspath(os.path.expanduser(self.source))
        path, _ = os.path.splitext(source)
        basename = os.path.basename(str(path).rstrip("/"))

        # Zip the artifact if it is a directory
        if os.path.isdir(source):
            source = str(source).rstrip("/")
            # Runtime must have entrypoint if the source is a directory
            if not self.runtime.entrypoint:
                raise ValueError(
                    "Please specify entrypoint when script source is a directory."
                )
            output = os.path.join(self.temp_dir.name, basename)
            shutil.make_archive(
                output, "zip", os.path.dirname(source), base_dir=basename
            )
            self.path = output + ".zip"
            return
        # Otherwise, use the artifact directly
        self.path = source
