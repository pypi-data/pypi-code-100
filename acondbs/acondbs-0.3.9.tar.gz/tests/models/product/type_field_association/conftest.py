import pytest

from acondbs.db.sa import sa
from acondbs.models import ProductType, FieldType, Field, TypeFieldAssociation


##__________________________________________________________________||
@pytest.fixture
def app(app_empty):

    y = app_empty

    field1 = Field(name="field1", type_=FieldType.UnicodeText)
    field2 = Field(name="field2", type_=FieldType.Integer)

    type1 = ProductType(  # noqa: F841
        name="type1",
        fields=[
            TypeFieldAssociation(field=field1),
            TypeFieldAssociation(field=field2),
        ],
    )

    with y.app_context():
        sa.session.add(field1)
        sa.session.add(field2)
        sa.session.add(type1)
        sa.session.commit()

    yield y


##__________________________________________________________________||
