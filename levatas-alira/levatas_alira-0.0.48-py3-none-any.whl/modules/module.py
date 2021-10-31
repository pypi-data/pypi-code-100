class Module(object):
    def __init__(self, pipeline_module_name = None):
        
        if pipeline_module_name:
            self._pipeline_module_name = pipeline_module_name
