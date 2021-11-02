import datetime

from ...db.sa import sa


##__________________________________________________________________||
class Product(sa.Model):
    # TODO: rename the class name to be more generic, e.g., "Entry"
    # TODO: use singular for the table name
    __tablename__ = "products"
    product_id = sa.Column(sa.Integer(), primary_key=True)
    type_id = sa.Column(sa.ForeignKey("product_types.type_id"), nullable=False)
    type_ = sa.relationship("ProductType", backref=sa.backref("products"))
    name = sa.Column(sa.Text(), nullable=False)
    contact = sa.Column(sa.Text())  # TODO: move to attribute model
    date_produced = sa.Column(sa.Date())  # TODO: move to attribute model
    produced_by = sa.Column(sa.Text())  # TODO: move to attribute model
    time_posted = sa.Column(
        sa.DateTime(), default=lambda: datetime.datetime.now()
    )
    posted_by = sa.Column(sa.Text())
    posting_git_hub_user_id = sa.Column(sa.ForeignKey("github_users.user_id"))
    posting_git_hub_user = sa.relationship(
        "GitHubUser",
        foreign_keys=[posting_git_hub_user_id],
        backref=sa.backref("posted_products", cascade="all"),
    )
    time_updated = sa.Column(sa.DateTime())
    updated_by = sa.Column(sa.Text())
    updating_git_hub_user_id = sa.Column(sa.ForeignKey("github_users.user_id"))
    updating_git_hub_user = sa.relationship(
        "GitHubUser",
        foreign_keys=[updating_git_hub_user_id],
        backref=sa.backref("updated_products", cascade="all"),
    )
    note = sa.Column(sa.Text())
    __table_args__ = (
        sa.UniqueConstraint("type_id", "name", name="_type_id_name"),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name!r}>"


##__________________________________________________________________||
