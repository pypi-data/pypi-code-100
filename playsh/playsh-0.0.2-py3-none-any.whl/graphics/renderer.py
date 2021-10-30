from contextlib import contextmanager
from functools import cache
from typing import Final, Union
from collections.abc import Generator

import glm
import numpy
from glm import vec2, vec3
from injector import inject
from OpenGL import GL as gl
from playsh.error import (
    FragmentShaderIOError,
    GeometryInvalidPositions,
    ShaderAttributeNotFound,
)
from playsh.graphics.geometry import Geometry, ScreenQuad
from playsh.graphics.shader import Attribute as ShaderAttribute
from playsh.graphics.shader import Shader


class GpuBuffer:
    def __init__(self, geometry: Geometry, shader: Shader) -> None:
        if not geometry.positions:
            raise GeometryInvalidPositions()

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        def try_create_buffer_slot(
            geometry_attribute: Union[tuple[vec2], tuple[vec3], None],
            attribute: ShaderAttribute,
        ) -> None:
            if not geometry_attribute:
                return

            try:
                attrib_location = shader.attribute_location(attribute)
            except ShaderAttributeNotFound:
                return

            geometry_attribute_flat = [
                item for vertex in geometry_attribute for item in vertex
            ]
            vertices = numpy.array(geometry_attribute_flat, dtype=numpy.float32)
            vbo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
            gl.glBufferData(
                gl.GL_ARRAY_BUFFER, len(vertices) * 4, vertices, gl.GL_STATIC_DRAW
            )

            gl.glEnableVertexAttribArray(attrib_location)
            vertex_bytesize = glm.sizeof(geometry_attribute[0])
            vertex_component = gl.GL_FLOAT
            vertex_components_count = vertex_bytesize // 4
            gl.glVertexAttribPointer(
                attrib_location,
                vertex_components_count,
                vertex_component,
                False,
                vertex_bytesize,
                None,
            )

        try_create_buffer_slot(geometry.positions, ShaderAttribute.POSITION)
        try_create_buffer_slot(geometry.normals, ShaderAttribute.NORMAL)
        try_create_buffer_slot(geometry.texcoords, ShaderAttribute.TEXCOORD)

        gl.glBindVertexArray(0)

    def bind(self) -> None:
        if self.vao:
            gl.glBindVertexArray(self.vao)

    def unbind(self) -> None:
        gl.glBindVertexArray(0)

    def __enter__(self):
        self.bind()

    def __exit__(self, type, value, traceback):
        self.unbind()


class GeometryRenderer:
    def render(self, geometry: Geometry, shader: Shader) -> None:
        gpu_buffer = self._get_or_create_gpu_buffer(geometry, shader)

        @contextmanager
        def bind(resource: Union[GpuBuffer, Shader]) -> Generator:
            resource.bind()
            try:
                yield resource
            finally:
                resource.unbind()

        with bind(gpu_buffer), bind(shader):
            if geometry.indices:
                gl.glDrawElements(
                    geometry.topology, len(geometry.indices), gl.GL_UNSIGNED_INT, 0
                )
            else:
                gl.glDrawArrays(geometry.topology.value, 0, len(geometry.positions))

    @cache
    def _get_or_create_gpu_buffer(self, geometry: Geometry, shader: Shader):
        return GpuBuffer(geometry, shader)


class ScreenRenderer:
    @inject
    def __init__(self, geometry_renderer: GeometryRenderer) -> None:
        self.geometry_renderer = geometry_renderer
        self._vertex_shader_text: Final = """
        #version 330
        layout (location = 0) in vec3 IN_POSITION;
        layout (location = 1) in vec2 IN_TEXCOORD;

        out vec2 TEXCOORD;
        
        uniform vec3 iResolution;

        void main() {
            gl_Position = vec4(IN_POSITION, 1.0);
            TEXCOORD = iResolution.xy * IN_TEXCOORD;
        }
        """

    def render(
        self, fragment_shader_path: str, params: dict[str, Shader.ParamType]
    ) -> None:
        shader = self._get_or_create_shader(fragment_shader_path)
        for name, param in params.items():
            shader.try_param(name, param)
        self.geometry_renderer.render(ScreenQuad(), shader)

    @cache
    def _get_or_create_shader(self, fragment_shader_path: str) -> Shader:
        try:
            with open(fragment_shader_path, "r") as file:
                fragment_shader_text = file.read()
                return Shader.from_text(self._vertex_shader_text, fragment_shader_text)
        except IOError as e:
            raise FragmentShaderIOError(
                "Error reading file {} : {}".format(fragment_shader_path, repr(e))
            )
