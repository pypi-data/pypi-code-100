import pytest

import datetime

from acondbs.db.sa import sa
from acondbs.models import (
    ProductType,
    FieldType,
    Field,
    TypeFieldAssociation,
    Product,
    AttributeUnicodeText,
    AttributeDate,
    AttributeDateTime,
)


##__________________________________________________________________||
@pytest.fixture
def app(app_empty):

    y = app_empty

    # create fields
    field1 = Field(name="attr1", type_=FieldType.UnicodeText)
    field2 = Field(name="date_produced", type_=FieldType.Date)
    field3 = Field(name="time_posted", type_=FieldType.DateTime)
    fields = [field1, field2, field3]

    # create product types
    Map = ProductType(
        type_id=1,
        name="map",
        order=2,
        indef_article="a",
        singular="map",
        plural="maps",
        icon="mdi-map",
        fields=[TypeFieldAssociation(field=f) for f in fields],
    )
    Beam = ProductType(
        type_id=2,
        name="beam",
        order=1,
        indef_article="a",
        singular="beam",
        plural="beams",
        icon="mdi-spotlight-beam",
        fields=[TypeFieldAssociation(field=f) for f in fields],
    )

    # create products
    map1 = Product(product_id=1, name="map1", type_=Map)
    AttributeUnicodeText(product=map1, field=field1, name="attr1", value="value1")
    AttributeDate(
        product=map1, field=field2, name="date_produced", value=datetime.date(2020, 2, 1)
    )
    AttributeDateTime(
        product=map1,
        field=field3,
        name="time_posted",
        value=datetime.datetime(2020, 2, 1, 9, 10, 25),
    )
    map2 = Product(product_id=2, name="map2", type_=Map)
    AttributeUnicodeText(product=map2, field=field1, name="attr1", value="value2")
    AttributeDate(
        product=map2, field=field2, name="date_produced", value=datetime.date(2020, 2, 10)
    )
    AttributeDateTime(
        product=map2,
        field=field3,
        name="time_posted",
        value=datetime.datetime(2020, 2, 10, 13, 20, 2),
    )
    map3 = Product(product_id=3, name="map3", type_=Map)
    AttributeUnicodeText(product=map3, field=field1, name="attr1", value="value3")
    AttributeDate(
        product=map3, field=field2, name="date_produced", value=datetime.date(2020, 3, 19)
    )
    AttributeDateTime(
        product=map3,
        field=field3,
        name="time_posted",
        value=datetime.datetime(2020, 3, 20, 8, 45, 30),
    )
    beam1 = Product(product_id=4, name="beam1", type_=Beam)
    AttributeUnicodeText(product=beam1, field=field1, name="attr1", value="value4")
    AttributeDate(
        product=beam1, field=field2, name="date_produced", value=datetime.date(2020, 2, 5)
    )
    AttributeDateTime(
        product=beam1,
        field=field3,
        name="time_posted",
        value=datetime.datetime(2020, 2, 5, 12, 3, 48),
    )
    beam2 = Product(product_id=5, name="beam2", type_=Beam)
    AttributeUnicodeText(product=beam2, field=field1, name="attr1", value="value5")
    AttributeDate(
        product=beam2, field=field2, name="date_produced", value=datetime.date(2020, 3, 4)
    )
    AttributeDateTime(
        product=beam2,
        field=field3,
        name="time_posted",
        value=datetime.datetime(2020, 3, 4, 19, 22, 5),
    )

    with y.app_context():
        sa.session.add(Map)
        sa.session.add(Beam)
        sa.session.commit()

    yield y


##__________________________________________________________________||
