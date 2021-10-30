from typing import Dict, Union, Any
from pyscfg.stores import DataStore, RamStore, get_store
from pyscfg import PySCFGError

import logging
log = logging.getLogger(__file__)


class ConfigsDictError(PySCFGError):
    pass


class ConfigsDictKeyError(ConfigsDictError):
    pass


class InvalidConfigsDictKeyFormatException(ConfigsDictError):

    def __init__(self, key):
        super().__init__(f"invalid key: '{key}' - key must be a string")


class ConfigsDict:

    def __init__(self,
                 data: Dict[str, Any] = None,
                 super_dict: "ConfigsDict" = None,
                 prefix: str = "",
                 data_store: DataStore = None):
        self._super_dict = super_dict
        self._prefix = prefix if not prefix.startswith(".") else prefix[1:]
        if prefix == "":
            self._data_store = data_store if data_store is not None else RamStore()
        else:
            self._data_store = None

        if self._data_store is not None:
            if data is not None:
                if not self._data_store.is_empty() \
                        and not self._flatten_dict(data) == self._flatten_dict(self._data_store.load()):
                    raise ValueError(f":param data: and :param data_store: are specified but the data "
                                     f"in the DataStore does not equal the data passed to the constructor.")
                else:
                    self._configs = self._flatten_dict(data)
                    self.save()
            else:
                self._configs = self._flatten_dict(self._data_store.load())
        else:
            self._configs = self._flatten_dict(data) if data is not None else dict()

    @property
    def configs(self):
        return self._configs

    @configs.setter
    def configs(self, value):
        self._configs = ConfigsDict._flatten_dict(value)

    def _get_subdict(self, key: str):
        levels = key.split(".")
        if len(levels) == 1:
            return ConfigsDict(self._filter_dict(self._configs, key),
                               super_dict=self,
                               prefix=".".join([self._prefix, key]))
        else:
            return ConfigsDict(self._filter_dict(self._configs, levels[0]),
                               super_dict=self,
                               prefix=".".join([self._prefix, levels[0]]))._get_subdict(".".join(levels[1:]))

    def save(self):
        if self._data_store is not None:
            self._data_store.save(self.as_dict())

    def is_empty(self) -> bool:
        return self._configs == {}

    def as_dict(self) -> dict:
        dict_repr = {}
        for k, v in self._configs.items():
            levels = k.split(".")
            dict_repr[levels[0]] = self._get_subdict(levels[0]).as_dict() if len(levels) > 1 else v

        return dict_repr

    def _get(self, key, as_dict: bool = False) -> Union["ConfigsDict", Any]:
        if not self._is_valid_key(key):
            raise InvalidConfigsDictKeyFormatException(key)
        levels = key.split(".")
        if len(levels) == 1:
            if key in self._configs.keys():
                return self._configs[key]
            else:
                subdict = self._get_subdict(key)
                if not subdict.is_empty():
                    return subdict.as_dict() if as_dict else subdict
                else:
                    raise KeyError(key)
        else:
            return self._get_subdict(levels[0])._get(".".join(levels[1:]), as_dict=as_dict)

    def get(self, key, default=None, as_dict: bool = True) -> Union["ConfigsDict", Any]:
        try:
            return self._get(key, as_dict=as_dict)
        except KeyError:
            return default

    def __getitem__(self, key):
        return self._get(key, as_dict=False)

    def _set(self, key, value):
        if not self._is_valid_key(key):
            raise InvalidConfigsDictKeyFormatException(key)
        self._configs.update(self._flatten_dict({key: value}))

        ConfigsDict.__update_super_dicts(self)

    def __setitem__(self, key, value):
        self._set(key, value)

    def _pop(self, key: str) -> Union["ConfigsDict", Any]:
        levels = key.split(".")
        if len(levels) > 1:
            key = levels[-1]
            c_dict = self._get_subdict(".".join(levels[:-1]))
        else:
            c_dict = self

        new_dict = c_dict.as_dict()
        try:
            removed_key = new_dict.pop(key)
        except KeyError:
            raise KeyError(".".join(levels))

        c_dict._configs = ConfigsDict._flatten_dict(new_dict)
        ConfigsDict.__update_super_dicts(c_dict)

        return ConfigsDict(removed_key, c_dict, prefix=key) if isinstance(removed_key, dict) else removed_key

    def pop(self, key, default=None):
        try:
            return self._pop(key)
        except KeyError:
            return default

    def remove(self, key: str) -> None:
        self._pop(key)

    def __delitem__(self, key: str) -> None:
        self._pop(key)

    def __iter__(self):
        for k, v in self.configs.items():
            yield k, v

    def __repr__(self):
        return self._configs

    def __str__(self):
        return f"ConfigsDict({str(self._configs)}"\
            f",\n\tstore:{type(self._data_store) if self._data_store is not None else None})"

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    @staticmethod
    def _is_valid_key(key):
        """
        Check if :param key: is valid (is string).
        :return:
        """
        if not isinstance(key, str):
            return False
        # possibly add other checks
        return True

    @staticmethod
    def _filter_dict(d:Dict[str, Any], prefix: str) -> Dict[str, Any]:
        return {k[len(prefix)+1:]: v for k,v in d.items() if k.startswith(f"{prefix}.")}

    @staticmethod
    def _flatten_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten a dict as subdict keys are merged into the dict using a '.' to separate different levels.
        :param data: the dict to flatten
        :return:
        """
        subdicts = [k for k, v in data.items() if isinstance(v, (dict, ConfigsDict))]

        for k in data.keys():
            if not ConfigsDict._is_valid_key(k):
                raise ValueError(f"invalid key: '{k}'")

        flattened_dict = {f"{k}.{sub_k}": sub_v for k in subdicts
                          for sub_k, sub_v in ConfigsDict._flatten_dict(data[k]).items()}
        flattened_dict.update({k: v for k,v in data.items() if not isinstance(v, (dict, ConfigsDict))})

        return flattened_dict

    @staticmethod
    def __update_super_dicts(d: "ConfigsDict"):
        """
        recursively update the super dicts of :param d:
        """
        while d._super_dict is not None:
            d_ = d._super_dict

            new_dict = d_.as_dict()
            new_dict.update({d._prefix.split(".")[-1]: d._configs})
            d_._configs = ConfigsDict._flatten_dict(new_dict)
            d = d_

        # save changes to base dict
        d.save()


class SimpleConfigs(ConfigsDict):

    def __init__(self, file: str = "configs.yml", store_type: str = "auto", defaults: Union[dict, str] = None):

        store = get_store(filename=file, store_type=store_type)

        data = {}
        # init the configs with some default values if there are no values stored for this values
        if defaults:
            if isinstance(defaults, str):
                defaults = get_store(filename=defaults).load()
            data = defaults

        store_data = store.load()
        data.update(store_data)

        super().__init__(data=data, data_store=store)

    def __repr__(self):
        return f"SimpleConfigs({str(self._configs)} \
            ,\n\tstore:{type(self._data_store) if self._data_store is not None else self._data_store})"
