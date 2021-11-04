def sig_disable(hub, tunnel_plugin, target_name, service):
    ...


def sig_enable(hub, tunnel_plugin, target_name, service):
    ...


def sig_start(hub, tunnel_plugin, target_name, service, **kwargs):
    ...


def sig_stop(hub, tunnel_plugin, target_name, service):
    ...


def sig_restart(hub, tunnel_plugin, target_name, service):
    ...


def sig_clean(hub, target_name, tunnel_plugin):
    ...


def pre(hub, ctx):
    kwargs = ctx.get_arguments()
    if ctx.func.__name__ in ["clean", "get_service_plugin", "valid_service_names"]:
        return True
    service_name = kwargs.get("service")
    if ctx.func.__name__ in ["service_conf_path", "clean", "conf_path"]:
        service_name = kwargs.get("service_name")
    valid_names = hub.service.init.valid_service_names()
    if service_name not in valid_names:
        raise ValueError(
            f"The service name {service_name} is not a valid name. "
            f"Please choose from the following: {valid_names}"
        )
