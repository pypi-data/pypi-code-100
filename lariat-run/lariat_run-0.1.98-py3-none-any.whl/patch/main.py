import logging

log = logging.getLogger(__name__)


def patch_all():
    try:
        import lariat.patch.pandas as patch_pandas

        patch_pandas.patch()
    except Exception as e:
        log.warning("Couldn't patch module pandas %s", e)

    try:
        import lariat.patch.sklearn as patch_sklearn

        patch_sklearn.patch()
    except Exception:
        log.warning("Couldn't patch module sklearn")

    try:
        import lariat.patch.subprocess as patch_subprocess

        #patch_subprocess.patch()
    except Exception:
        log.warning("Couldn't patch module subprocess")

    try:
        import lariat.patch.flask as patch_flask

        patch_flask.patch()
    except Exception:
        log.warning("Couldn't patch module flask")

    try:
        import lariat.patch.sqlalchemy as patch_sqlalchemy

        patch_sqlalchemy.patch()
    except Exception:
        log.warning("Couldn't patch module sqlalchemy %s", e)
