from box import Box
from jupyterbundle.server_detector import is_jupyter_server_running
from pyfonybundles.Bundle import Bundle


class JupyterBundle(Bundle):
    def modify_parameters(self, parameters: Box) -> Box:
        if is_jupyter_server_running():
            parameters.pysparkbundle.dataframe.show_method = "jupyter_display"
            parameters.daipecore.pandas.dataframe.show_method = "jupyter_display"

        return parameters
