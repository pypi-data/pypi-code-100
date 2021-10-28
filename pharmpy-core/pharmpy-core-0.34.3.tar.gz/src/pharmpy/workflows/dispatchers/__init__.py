import pharmpy.config as config

from .local import LocalDispatcher


class DispatcherConfiguration(config.Configuration):
    module = 'pharmpy.workflows.dispatchers'
    dask_dispatcher = config.ConfigItem(
        None,
        'Which type of dask scheduler to use (supports threaded and distributed).',
        str,
    )


conf = DispatcherConfiguration()


__all__ = ['LocalDispatcher']
