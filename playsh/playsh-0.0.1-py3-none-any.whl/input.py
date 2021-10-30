from glm import vec2
import glfw


class Input:
    def __init__(self) -> None:
        KEYS_COUNT = glfw.KEY_LAST + 1
        self.keys = [glfw.RELEASE] * KEYS_COUNT
        self.prev_keys = self.keys.copy()

        MOUSE_KEYS_COUNT = glfw.MOUSE_BUTTON_LAST + 1
        self.mouse_keys = [glfw.RELEASE] * MOUSE_KEYS_COUNT
        self.prev_mouse_keys = self.mouse_keys.copy()

        self.cursor_pos: vec2 = vec2(0.0)

    def update(self) -> None:
        self.prev_keys = self.keys.copy()
        self.prev_mouse_keys = self.mouse_keys.copy()

    def is_key_down(self, key: int) -> bool:
        return self.keys[key] == glfw.PRESS

    def is_key_pressed(self, key: int) -> bool:
        return self.keys[key] == glfw.PRESS and self.prev_keys[key] == glfw.RELEASE

    def is_mouse_key_down(self, key: int) -> bool:
        return self.mouse_keys[key] == glfw.PRESS

    def is_mouse_key_pressed(self, key: int) -> bool:
        return (
            self.mouse_keys[key] == glfw.PRESS
            and self.prev_mouse_keys[key] == glfw.RELEASE
        )

    def on_key_changed(self, key: int, scan_code: int, action: int, mods: int) -> None:
        # NOTE(panmar): glfw.REPEAT is converted to glfw.PRESS
        self.keys[key] = glfw.RELEASE if (action == glfw.RELEASE) else glfw.PRESS

    def on_mouse_key_changed(self, key: int, action: int, mods: int) -> None:
        self.mouse_keys[key] = glfw.RELEASE if action == glfw.RELEASE else glfw.PRESS

    def on_cursor_pos_changed(self, x: int, y: int) -> None:
        self.cursor_pos = vec2(x, y)
