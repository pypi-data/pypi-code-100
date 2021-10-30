from enum import Enum
from functools import cache
from pathlib import Path
from typing import Union

import glm
from glm import mat4, vec2, vec3, vec4, array
from OpenGL import GL as gl
from playsh.error import (
    ShaderAttributeNotFound,
    ShaderCompilationError,
    ShaderInvalidParamType,
    ShaderInvalidParamValue,
    ShaderInvalidProgram,
    ShaderLinkageError,
    ShaderUniformNotFound,
)
from playsh.graphics.texture import Texture


class Attribute(Enum):
    POSITION = "IN_POSITION"
    NORMAL = "IN_NORMAL"
    TEXCOORD = "IN_TEXCOORD"


class Shader:
    def __init__(self, program: int = 0):
        self.program = program
        self.current_sampler_slot: int = 0

    @staticmethod
    def from_file(vs_path: Path, fs_path: Path) -> "Shader":
        with open(vs_path, "r") as vs_file, open(fs_path, "r") as fs_file:
            vs_text = vs_file.read()
            fs_text = fs_file.read()
        return Shader.from_text(vs_text, fs_text)

    @staticmethod
    @cache
    def from_text(vs_text: str, fs_text: str) -> "Shader":
        def create_shader(text: str, type: int) -> int:
            shader = gl.glCreateShader(type)
            gl.glShaderSource(shader, text)
            gl.glCompileShader(shader)
            return shader

        def check_compilation_errors(shader: int) -> None:
            status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
            if not status:
                error = gl.glGetShaderInfoLog(shader)
                raise ShaderCompilationError(error)

        vs = create_shader(vs_text, gl.GL_VERTEX_SHADER)
        check_compilation_errors(vs)
        fs = create_shader(fs_text, gl.GL_FRAGMENT_SHADER)
        check_compilation_errors(fs)

        program = gl.glCreateProgram()
        gl.glAttachShader(program, vs)
        gl.glAttachShader(program, fs)
        gl.glLinkProgram(program)

        def check_linkage_errors(program: int) -> None:
            status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
            if not status:
                error = gl.glGetProgramInfoLog(program)
                raise ShaderLinkageError(error)

        check_linkage_errors(program)

        return Shader(program)

    def attribute_location(self, attribute: Attribute) -> int:
        if not self.program:
            raise ShaderInvalidProgram()

        location = gl.glGetAttribLocation(self.program, attribute.value)
        if location == -1:
            raise ShaderAttributeNotFound(
                "Shader attribute {} not found".format(attribute.value)
            )

        return location

    ParamType = Union[int, float, vec2, vec3, vec4, mat4, array, Texture]

    def param(self, name: str, value: ParamType) -> "Shader":
        location = gl.glGetUniformLocation(self.program, name)
        if location == -1:
            raise ShaderUniformNotFound("Shader attribute {} not found".format(name))
        self.bind()
        if isinstance(value, int):
            gl.glUniform1i(location, value)
        elif isinstance(value, float):
            gl.glUniform1f(location, value)
        elif isinstance(value, vec2):
            gl.glUniform2f(location, *value)
        elif isinstance(value, vec3):
            gl.glUniform3f(location, *value)
        elif isinstance(value, vec4):
            gl.glUniform4f(location, *value)
        elif isinstance(value, mat4):
            gl.glUniformMatrix4fv(location, 1, True, glm.value_ptr(value))
        elif isinstance(value, array):
            if len(value) == 0:
                raise ShaderInvalidParamValue("Shader array parameter is empty")
            # NOTE(panmar): We assume that array stores the same types
            array_type = type(value[0])
            if array_type == glm.vec2:
                gl.glUniform2fv(location, len(value), value.ptr)
            elif array_type == glm.vec3:
                gl.glUniform3fv(location, len(value), value.ptr)
            elif array_type == glm.vec4:
                gl.glUniform4fv(location, len(value), value.ptr)
            else:
                raise ShaderInvalidParamType(
                    "Parameter array[{}] is unsupported".format(array_type)
                )
        elif isinstance(value, Texture):
            value.bind()
            self.param(name, self.current_sampler_slot)
            self.current_sampler_slot = self.current_sampler_slot + 1
        else:
            raise ShaderInvalidParamType(
                "Parameter {} is unsupported".format(type(value))
            )

        return self

    def try_param(self, name: str, value) -> "Shader":
        try:
            return self.param(name, value)
        except ShaderUniformNotFound:
            return self

    def bind(self) -> "Shader":
        if not self.program:
            raise ShaderInvalidProgram()
        gl.glUseProgram(self.program)
        self.current_sampler_slot = 0
        return self

    def unbind(self) -> "Shader":
        gl.glUseProgram(0)
        return self
