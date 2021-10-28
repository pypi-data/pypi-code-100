import hashlib
from typing import List, Optional, Any
from pydantic import BaseModel


class FormFieldValidation(BaseModel):
    regex: str
    message: str


class FormComponent(BaseModel):
    type: str = 'text'
    props: Optional[dict] = {}


class FormField(BaseModel):
    id: str
    name: str
    description: Optional[str]
    component: FormComponent
    validation: Optional[FormFieldValidation]
    required: bool = False


class FormGroup(BaseModel):
    name: Optional[str]
    description: Optional[str]
    fields: List[FormField]


class Form(BaseModel):
    title: Optional[str]
    groups: List[FormGroup]


class Spec(BaseModel):
    id: Optional[str]
    className: str
    module: str
    inputs: Optional[List[str]] = []
    outputs: Optional[List[str]] = []
    init: Optional[dict] = None
    onErrorContinue: bool = False
    onErrorRepeat: int = 1
    form: Optional[Form]
    manual: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = "MIT"
    version: Optional[str] = '0.0.1'

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.id = self.get_id()

    def get_id(self) -> str:
        action_id = self.module + self.className
        return hashlib.md5(action_id.encode()).hexdigest()


class MetaData(BaseModel):
    name: str
    desc: Optional[str] = ""
    keywords: Optional[List[str]] = []
    type: str
    width: int
    height: int
    icon: str
    editor: str = 'json'
    group: Optional[List[str]] = ["General"]


class Plugin(BaseModel):
    start: bool = False
    debug: bool = False
    spec: Spec
    metadata: MetaData
