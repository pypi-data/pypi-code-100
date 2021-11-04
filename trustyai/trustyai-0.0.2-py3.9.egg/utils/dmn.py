"""Utilities to handle DMN models and runtimes"""

from org.kie.dmn.api.core import DMNRuntime
from org.kie.kogito.dmn import DMNKogito
from org.kie.kogito.decision import DecisionModel
from java.io import InputStreamReader, ByteArrayInputStream


def createModel(file: str) -> DecisionModel:
    contents = open(file, 'r').read()
    _dmnRuntime = DMNKogito.createGenericDMNRuntime(InputStreamReader(ByteArrayInputStream(contents.getBytes())))
        