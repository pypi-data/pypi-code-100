from typing import Dict, List, Optional, Any

from pydantic import BaseModel


class TransformArgumentCreate(BaseModel):
    name: str
    description: str
    type: str


class TransformCreate(BaseModel):
    name: Optional[str]
    sourceCode: str
    description: Optional[str]
    arguments: Optional[List[TransformArgumentCreate]]


class Transform(TransformCreate):
    id: Optional[int]
    arguments: Optional[List]


# Utilities
class TransformUtilityDefinition(BaseModel):
    name: str
    description: str
    arguments: Dict[str, str]


class TransformUtility(BaseModel):
    name: str
    arguments: Dict[str, str]
    resultArgumentName: str


# Transform Execution
class TransformArgs(BaseModel):
    """
    Schema/contract for Executing a Transform
    """
    transformId: Optional[int]
    sourceCode: Optional[str]
    arguments: Dict[str, Any]
    utilities: Optional[List[TransformUtility]]


class TransformExecute(BaseModel):
    """
    Contract for execution of one or more transforms
    """
    dataSourceId: int
    newTableName: Optional[str]
    transformArgs: List[TransformArgs]
