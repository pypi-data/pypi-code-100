from django.db import (
    models,
)

from m3_gar.base_models import (
    AdmHierarchy as BaseAdmHierarchy,
    MunHierarchy as BaseMunHierarchy,
)
from m3_gar.models.reestr import (
    ReestrObjects,
)
from m3_gar.models.util import (
    RegionCodeModelMixin,
    make_fk,
)


__all__ = ['AdmHierarchy', 'MunHierarchy']


class Hierarchy:
    """
    Базовый тип сведений по иерархии
    """

    @staticmethod
    def get_shortname_map():
        return {
            subclass.get_shortname(): subclass
            for subclass in Hierarchy.__subclasses__()
        }

    @classmethod
    def get_shortname(cls):
        shortname = ''

        if cls.__name__.endswith(Hierarchy.__name__):
            shortname = cls.__name__[:-len(Hierarchy.__name__)]

        return shortname.lower()


class AdmHierarchy(BaseAdmHierarchy, Hierarchy, RegionCodeModelMixin):
    """
    Сведения по иерархии в административном делении
    """
    class Meta:
        verbose_name = verbose_name_plural = 'Иерархия в административном делении'


class MunHierarchy(BaseMunHierarchy, Hierarchy, RegionCodeModelMixin):
    """
    Сведения по иерархии в муниципальном делении
    """
    class Meta:
        verbose_name = verbose_name_plural = 'Иерархия в муниципальном делении'


make_fk(AdmHierarchy, 'objectid', to=ReestrObjects)
make_fk(MunHierarchy, 'objectid', to=ReestrObjects)

make_fk(AdmHierarchy, 'parentobjid', to=ReestrObjects)
make_fk(MunHierarchy, 'parentobjid', to=ReestrObjects)
