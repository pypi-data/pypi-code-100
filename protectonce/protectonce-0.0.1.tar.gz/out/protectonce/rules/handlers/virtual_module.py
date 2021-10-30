from ..types.class_rule import ClassRule


class VirtualModule(object):
    _virtual_modules = {}

    def __init__(self, rule) -> None:
        super().__init__()
        self._rule = rule
        self._interceptor = None

    @staticmethod
    def register(rule) -> None:
        intercept = rule.get('intercept', {})
        module = intercept.get('module', '')
        if not module:
            print('intercept.module is must for creation of virtual module')

        virtual_module = VirtualModule._virtual_modules.get(module, None)
        if virtual_module:
            print(f'virtual module {module} already registered!')
            return

        VirtualModule._virtual_modules[module] = VirtualModule(rule)

    @staticmethod
    def create(config, args, kwargs, result) -> None:
        virtual_module = VirtualModule.__get_cached_module(config)
        context = VirtualModule.__get_context(config, args, result)

        if not virtual_module or not context:
            return
        virtual_module.__add_interceptors(context)

    @staticmethod
    def __get_cached_module(config):
        module = config.get('virtualModule', '')
        if not module:
            return None

        return VirtualModule._virtual_modules[module]

    @staticmethod
    def __get_context(config, args, result):
        if result:
            # FIXME: Assuming after handler represents context in result
            return result

        # TODO: What if context is in kwargs??
        index = config.get('moduleInstanceIndex', -1)
        if index == -1 or len(args) <= index:
            print(f'Invalid moduleInstanceIndex specified: {index}')
            return

        return args[index]

    def __add_interceptors(self, context):
        self._class_rule = ClassRule(self._rule, context)
        self._class_rule.add_instrumentation()
        pass
