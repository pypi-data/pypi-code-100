from sqlalchemy import create_engine, inspect

from flowingo.models.base import Session, engine, init


class TestDatabase:
    TABLE_NAMES = [
        'pipeline', 'pipeline_run', 'pipeline_tag', 'pipeline_dump',
        'task', 'task_tag', 'task_group',
        'user'
    ]

    def test_init(self):
        # Init database
        init()

        # Check tables
        inspect_obj = inspect(engine)
        assert set(inspect_obj.get_table_names()) == set(self.TABLE_NAMES)

