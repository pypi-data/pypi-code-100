from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import declarative_mixin

from ...db.sa import sa


##__________________________________________________________________||
@declarative_mixin
class AttributeBase:
    attribute_id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.Text())  # TODO: Remove

    @declared_attr
    def product_id(self):
        return sa.Column(sa.Integer(), sa.ForeignKey("products.product_id"), nullable=False)  # fmt: skip

    @declared_attr
    def product(self):
        return sa.relationship(
            "Product",
            backref=sa.backref(self.backref_column, cascade="all, delete-orphan"),  # fmt: skip
        )

    @declared_attr
    def field_id(self):
        return sa.Column(sa.Integer(), sa.ForeignKey("field.field_id"), nullable=True)  # fmt: skip
        # TODO: Make nullable False

    @declared_attr
    def field(self):
        return sa.relationship(
            "Field",
            backref=sa.backref(self.backref_column, cascade="all, delete-orphan"),  # fmt: skip
        )

    def __repr__(self):
        field_name = self.field.name if self.field else self.field
        return f"<{self.__class__.__name__} {field_name!r}: {self.value!r}>"


##__________________________________________________________________||
class AttributeUnicodeText(AttributeBase, sa.Model):
    __tablename__ = "attribute_unicode_text"
    backref_column = "attributes_unicode_text"
    value = sa.Column(sa.UnicodeText())


class AttributeBoolean(AttributeBase, sa.Model):
    __tablename__ = "attribute_boolean"
    backref_column = "attributes_boolean"
    value = sa.Column(sa.Boolean())


class AttributeInteger(AttributeBase, sa.Model):
    __tablename__ = "attribute_integer"
    backref_column = "attributes_integer"
    value = sa.Column(sa.Integer())


class AttributeFloat(AttributeBase, sa.Model):
    __tablename__ = "attribute_float"
    backref_column = "attributes_float"
    value = sa.Column(sa.Float())


class AttributeDate(AttributeBase, sa.Model):
    __tablename__ = "attribute_date"
    backref_column = "attributes_date"
    value = sa.Column(sa.Date())


class AttributeDateTime(AttributeBase, sa.Model):
    __tablename__ = "attribute_date_time"
    backref_column = "attributes_date_time"
    value = sa.Column(sa.DateTime())


class AttributeTime(AttributeBase, sa.Model):
    __tablename__ = "attribute_time"
    backref_column = "attributes_time"
    value = sa.Column(sa.Time())


##__________________________________________________________________||
