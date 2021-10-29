from django.contrib.postgres.indexes import (
    BTreeIndex,
    HashIndex,
)

from m3_gar.base_models import (
    AddrObj as BaseAddrObj,
    AddrObjDivision as BaseAddrObjDivision,
    AddrObjTypes as BaseAddrObjTypes,
)
from m3_gar.models.op_type import (
    OperationTypes,
)
from m3_gar.models.reestr import (
    ReestrObjects,
)
from m3_gar.models.util import (
    RegionCodeModelMixin,
    add_params,
    make_fk,
)


__all__ = ['AddrObj', 'AddrObjDivision', 'AddrObjTypes']


class AddrObjDivision(BaseAddrObjDivision, RegionCodeModelMixin):
    """
    Сведения по операциям переподчинения
    """
    class Meta:
        verbose_name = 'Операция переподчинения'
        verbose_name_plural = 'Операции переподчинения'


class AddrObjTypes(BaseAddrObjTypes):
    """
    Сведения по типам адресных объектов
    """
    class Meta:
        verbose_name = 'Тип адресного объекта'
        verbose_name_plural = 'Типы адресных объектов'


class AddrObj(BaseAddrObj, RegionCodeModelMixin):
    """
    Сведения классификатора адресообразующих элементов
    """
    class Meta:
        verbose_name = 'Адресообразующий элемент'
        verbose_name_plural = 'Адресообразующие элементы'

        indexes = (
            HashIndex(
                fields=('objectguid',),
            ),
            BTreeIndex(
                fields=('isactive', 'isactual', 'level'),
            )
        )


# На момент описания моделей AddrObjTypes никак не связывается с AddrObj
# Существующее поле AddrObj.typename - текстовое представление (ул, пер, г, и т.п.)
# make_fk(AddrObj, '???', to=AddrObjTypes, null=True, blank=True)

make_fk(AddrObjDivision, 'parentid', to=ReestrObjects, db_constraint=False)
make_fk(AddrObjDivision, 'childid', to=ReestrObjects, db_constraint=False)

make_fk(AddrObj, 'opertypeid', to=OperationTypes)
make_fk(AddrObj, 'objectid', to=ReestrObjects)

add_params(AddrObj, 'm3_gar.AddrObjParams')
