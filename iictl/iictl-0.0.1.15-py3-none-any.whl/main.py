# import iictl
from iictl.commands.main import cli
from kubernetes.config.kube_config import (
    KUBE_CONFIG_DEFAULT_LOCATION,
    _get_kube_config_loader,
    Configuration,
)

def entrypoint():
    _, namespace = load_kube_config()
    
    obj = {}
    if namespace is not None:
        obj['namespace'] = namespace
        
    cli(obj=obj)
    
def load_kube_config(config_file=None, context=None,
                     client_configuration=None,
                     persist_config=True):
    if config_file is None:
        config_file = KUBE_CONFIG_DEFAULT_LOCATION

    loader = _get_kube_config_loader(
        filename=config_file, active_context=context,
        persist_config=persist_config)

    if client_configuration is None:
        config = type.__call__(Configuration)
        loader.load_and_set(config)
        Configuration.set_default(config)
    else:
        loader.load_and_set(client_configuration)

    namespace = None
    if loader is not None and 'context' in loader.current_context and 'namespace' in loader.current_context['context']:
        namespace = loader.current_context['context']['namespace']
        
    return config, namespace
    
if __name__ == '__main__':
    entrypoint()