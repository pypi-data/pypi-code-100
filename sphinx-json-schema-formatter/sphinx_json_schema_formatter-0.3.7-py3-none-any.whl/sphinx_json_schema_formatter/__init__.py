from .directive import JsonSchema


def setup(app) -> None:
    app.add_directive("json-schema", JsonSchema)
    app.add_config_value("json_schema_root_dir", None, "env")
