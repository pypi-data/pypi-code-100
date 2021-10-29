import json

from ...db.sa import sa

from ..funcs import shorten


##__________________________________________________________________||
class WebConfig(sa.Model):
    __tablename__ = "web_config"
    id_ = sa.Column(sa.Integer(), primary_key=True)
    json = sa.Column(sa.Text())

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id_!r} {self._json_repr!r}>"

    @property
    def _json_repr(self):
        try:
            most_compact = json.dumps(json.loads(self.json), indent=None)
            return shorten(most_compact, width=20)
        except BaseException:
            pass

        try:
            return shorten(repr(self.json), width=20)
        except BaseException:
            pass

        return self.json


##__________________________________________________________________||
class WebConfigOld(sa.Model):
    __tablename__ = "web_config_old"
    config_id = sa.Column(sa.Integer(), primary_key=True)
    head_title = sa.Column(sa.Text())
    toolbar_title = sa.Column(sa.Text())
    devtool_loadingstate = sa.Column(sa.Boolean())
    product_creation_dialog = sa.Column(sa.Boolean())
    product_update_dialog = sa.Column(sa.Boolean())
    product_deletion_dialog = sa.Column(sa.Boolean())


##__________________________________________________________________||
