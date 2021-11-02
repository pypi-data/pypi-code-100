from ...db.sa import sa


##__________________________________________________________________||
class TypeFieldAssociation(sa.Model):
    __tablename__ = "type_field_association"
    iid = sa.Column(sa.Integer(), primary_key=True)
    type_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey("product_types.type_id"),
    )
    field_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey("field.field_id"),
        nullable=False,
    )
    type_ = sa.relationship(
        "ProductType",
        backref=sa.backref("fields", cascade="all, delete-orphan"),
    )
    field = sa.relationship(
        "Field",
        backref=sa.backref("entry_types"),
    )

    __table_args__ = (
        sa.UniqueConstraint("type_id", "field_id", name="_type_field"),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.type_name!r} {self.field_name!r}>"

    @property
    def type_name(self):
        # used in __repr__()
        try:
            return self.type_.name
        except BaseException:
            return self.type_

    @property
    def field_name(self):
        # used in __repr__()
        try:
            return self.field.name
        except BaseException:
            return self.field


##__________________________________________________________________||
