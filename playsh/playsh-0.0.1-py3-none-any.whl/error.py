class PlayShError(Exception):
    pass


class FragmentShaderIOError(PlayShError):
    pass


class GlfwError(PlayShError):
    pass


class GlfwInitError(PlayShError):
    pass


class GlfwCreateWindowError(PlayShError):
    pass


class ShaderCompilationError(PlayShError):
    pass


class ShaderLinkageError(PlayShError):
    pass


class ShaderAttributeNotFound(PlayShError):
    pass


class ShaderUniformNotFound(PlayShError):
    pass


class ShaderInvalidProgram(PlayShError):
    pass


class ShaderInvalidParamType(PlayShError):
    pass


class ShaderInvalidParamValue(PlayShError):
    pass


class GeometryInvalidPositions(PlayShError):
    pass
