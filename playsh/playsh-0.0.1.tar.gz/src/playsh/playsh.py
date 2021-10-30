import time
from dataclasses import dataclass
from sys import platform as _platform
from typing import Any

import glfw
from glm import array, vec3, vec4
from injector import Injector, inject
from OpenGL import GL as gl

from playsh.error import GlfwCreateWindowError, GlfwInitError
from playsh.graphics.renderer import ScreenRenderer
from playsh.graphics.shader import Shader
from playsh.graphics.texture import Texture, TextureDesc
from playsh.input import Input
from playsh.store import Store
from playsh.timer import Timer


@inject
@dataclass
class System:
    input: Input
    screen_renderer: ScreenRenderer
    timer: Timer
    frame_index: int = 0


class PlaySh:
    def __init__(
        self,
        width: int,
        height: int,
        fragment_shader_path: str,
        channel0: TextureDesc = None,
        channel1: TextureDesc = None,
        channel2: TextureDesc = None,
        channel3: TextureDesc = None,
    ) -> None:

        self._system = Injector().get(System)
        self._window = self._create_window(width, height, "PlaySh")
        glfw.make_context_current(self._window)

        self._setup_glfw_callbacks()

        # NOTE(panmar): On retina monitors pixel size can be different then window size
        self._width, self._height = glfw.get_framebuffer_size(self._window)

        self._fragment_shader_path = fragment_shader_path

        self.channels = [
            Texture(channel0) if channel0 else None,
            Texture(channel1) if channel1 else None,
            Texture(channel2) if channel2 else None,
            Texture(channel3) if channel3 else None,
        ]

    def _create_window(self, width: int, height: int, title: str) -> Any:
        if not glfw.init():
            raise GlfwInitError()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

        if _platform == "darwin":
            # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        window = glfw.create_window(width, height, title, None, None)
        if not window:
            glfw.terminate()
            raise GlfwCreateWindowError()

        return window

    def _setup_glfw_callbacks(self):
        glfw.set_key_callback(
            self._window,
            lambda _, *args: self._system.input.on_key_changed(*args),
        )

        glfw.set_mouse_button_callback(
            self._window,
            lambda _, *args: self._system.input.on_mouse_key_changed(*args),
        )

        glfw.set_cursor_pos_callback(
            self._window,
            lambda _, *args: self._system.input.on_cursor_pos_changed(*args),
        )

        glfw.set_framebuffer_size_callback(
            self._window, lambda _, *args: self._on_framebuffer_size_change(*args)
        )

    def _on_framebuffer_size_change(self, width: int, height: int):
        # NOTE(panmar): On retina monitors pixel size can be different then screen size
        self._width, self._height = glfw.get_framebuffer_size(self._window)

    def _update(self) -> None:
        self._system.timer.tick()
        self._system.frame_index = self._system.frame_index + 1

        if self._system.input.is_key_pressed(glfw.KEY_ESCAPE):
            glfw.set_window_should_close(self._window, True)

    def _collect_builtin_params(self) -> dict[str, Shader.ParamType]:
        params: dict[str, Shader.ParamType] = dict()
        params["iResolution"] = vec3(self._width, self._height, 0.0)
        params["iTime"] = self._system.timer.total_elapsed_seconds
        params["iTimeDelta"] = self._system.timer.elapsed_seconds
        params["iFrame"] = self._system.frame_index

        input = self._system.input
        params["iMouse"] = vec4(
            input.cursor_pos.x
            if input.is_mouse_key_down(glfw.MOUSE_BUTTON_LEFT)
            else 0.0,
            input.cursor_pos.y
            if input.is_mouse_key_down(glfw.MOUSE_BUTTON_LEFT)
            else 0.0,
            input.cursor_pos.x
            if input.is_mouse_key_pressed(glfw.MOUSE_BUTTON_LEFT)
            else 0.0,
            input.cursor_pos.y
            if input.is_mouse_key_pressed(glfw.MOUSE_BUTTON_LEFT)
            else 0.0,
        )

        for index, channel in enumerate(self.channels):
            if channel:
                params["iChannel{}".format(index)] = channel

        params["iChannelResolution"] = [
            vec3(ch.width, ch.height, 0.0) if ch else vec3(0.0) for ch in self.channels
        ]

        return params

    def _render(self) -> None:
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glViewport(0, 0, self._width, self._height)

        self._system.screen_renderer.render(
            self._fragment_shader_path, self._collect_builtin_params()
        )

    def run(self) -> None:
        while not glfw.window_should_close(self._window):
            self._update()
            self._render()

            def sleep_until_end_of_frame(frame_rate: int):
                frame_time = 1.0 / frame_rate
                sleep_time = self._system.timer.seconds_since_tick() - frame_time
                if sleep_time > 0.0:
                    time.sleep(sleep_time)

            sleep_until_end_of_frame(frame_rate=30)
            glfw.swap_buffers(self._window)
            glfw.poll_events()

        glfw.terminate()
