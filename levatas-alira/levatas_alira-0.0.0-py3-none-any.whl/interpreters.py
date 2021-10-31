import os


def translate_pipeline_modules_list(modules: list):
    for module in modules:
        if isinstance(module, dict) and "module" in module:
            module["class"] = module["module"]
        else:
            raise ValueError("All of the pipeline component must be a module.")

    return modules

def translate_pipeline_database(database: dict, model_base_directory: str):
    if "DATABASE_FILE" in database:
        alira_base_directory = os.path.dirname(model_base_directory)
        database["DATABASE_FILE"] = os.path.join(alira_base_directory, database["DATABASE_FILE"])

    return database


def translate_pipeline_configuration(configuration: dict, model_base_directory: str):
    configuration["pipeline"] = translate_pipeline_modules_list(
        configuration.get("pipeline", [])
    )

    configuration["database"] = (
        translate_pipeline_database(configuration["database"], model_base_directory)
        if "database" in configuration
        else {}
    )

    return configuration
