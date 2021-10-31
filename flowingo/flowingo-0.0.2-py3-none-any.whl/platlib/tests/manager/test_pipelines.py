import pathlib
import shutil
from copy import copy

import pytest
from pytest_mock import MockerFixture
from sqlalchemy import select

from flowingo.configuration import conf
from flowingo.manager.tasks.pipelines import refresh_all_pipelines, refresh_all_tasks, refresh_pipeline
from flowingo.models import Pipeline, PipelineDump, PipelineTag, Session, Task, TaskGroup, TaskTag


@pytest.mark.usefixtures("config_folders")
class TestRefreshAllTasks:
    GROUP_TASKS = {
        'first.yml': {'dummy', 'long_running_task', 'other_long_task'},
        'second.yml': {'sleep', 'setup'},
    }
    TAG_TASKS = {
        'long': {'long_running_task', 'other_long_task'},
        'second': {'sleep', 'setup'},
    }

    def test_read_valid_files(self, mocker: MockerFixture) -> None:
        patch = mocker.patch('flowingo.manager.tasks.pipelines._save_tasks_to_database')
        refresh_all_tasks()
        patch.assert_called_once()

        args, kwargs = patch.call_args
        assert len(args) == 1
        assert not kwargs
        tasks = args[0]
        assert tasks.keys() == self.GROUP_TASKS.keys()

        for task in tasks.values():
            assert isinstance(task, dict)

    def test_save_to_database(self, db_session_clear_tasks: Session) -> None:
        refresh_all_tasks()

        task_groups = db_session_clear_tasks.execute(select(TaskGroup)).scalars().all()
        assert {i.filename for i in task_groups} == self.GROUP_TASKS.keys()

        for group in task_groups:
            assert {i.name for i in group.tasks} == self.GROUP_TASKS[group.filename]

        task_tags = db_session_clear_tasks.execute(select(TaskTag)).scalars().all()
        assert {i.name for i in task_tags} == self.TAG_TASKS.keys()

        for tag_name, tag_tasks in self.TAG_TASKS.items():
            task_tags = db_session_clear_tasks.execute(select(TaskTag).where(TaskTag.name == tag_name)).scalars().all()
            assert {i.task.name for i in task_tags} == tag_tasks

    def test_delete_file(self, db_session_clear_tasks: Session, tmp_folder: pathlib.Path) -> None:
        task_folder, conf.tasks_folder = copy(conf.tasks_folder), copy(tmp_folder)

        # Load file
        shutil.copy(task_folder / 'first.yml', tmp_folder / 'current.yml')
        refresh_all_tasks()

        task_group = db_session_clear_tasks.execute(select(TaskGroup).where(TaskGroup.filename == 'current.yml')).scalar()
        assert {i.name for i in task_group.tasks} == self.GROUP_TASKS['first.yml']

        # Delete file
        (tmp_folder / 'current.yml').unlink()
        refresh_all_tasks()

        task_group = db_session_clear_tasks.execute(select(TaskGroup).where(TaskGroup.filename == 'current.yml')).scalar()
        assert not task_group

    def test_update_file(self, db_session_clear_tasks: Session, tmp_folder: pathlib.Path) -> None:
        task_folder, conf.tasks_folder = copy(conf.tasks_folder), copy(tmp_folder)

        # Load first file
        shutil.copy(task_folder / 'first.yml', tmp_folder / 'current.yml')
        refresh_all_tasks()
        db_session_clear_tasks.commit()  # TODO: why session does not update without it?
        db_session_clear_tasks.begin()

        task_group = db_session_clear_tasks.execute(select(TaskGroup).where(TaskGroup.filename == 'current.yml')).scalar()
        assert {i.name for i in task_group.tasks} == self.GROUP_TASKS['first.yml']

        # Load second file
        shutil.copy(task_folder / 'second.yml', tmp_folder / 'current.yml')
        refresh_all_tasks()
        refresh_all_tasks()
        db_session_clear_tasks.commit()  # TODO: why session does not update without it?
        db_session_clear_tasks.begin()

        task_group = db_session_clear_tasks.execute(select(TaskGroup).where(TaskGroup.filename == 'current.yml')).scalar()
        assert {i.name for i in task_group.tasks} == self.GROUP_TASKS['second.yml']


@pytest.mark.usefixtures("config_folders")
class TestRefreshPipelines:
    PIPELINES = {'first.yml', 'second.yml', 'sub.yml'}
    TAG_PIPELINES = {
        'sample': {'first.yml', 'second.yml'},
        'other': {'first.yml', 'sub.yml'},
    }

    def test_read_valid_files(self, mocker: MockerFixture) -> None:
        patch = mocker.patch('flowingo.manager.tasks.pipelines._save_pipelines_to_database')
        refresh_all_pipelines()
        patch.assert_called_once()

        args, kwargs = patch.call_args
        assert len(args) == 1
        assert kwargs == {'delete_missing': True}
        pipelines = args[0]
        assert pipelines.keys() == self.PIPELINES

        for task in pipelines.values():
            assert isinstance(task, dict)

    @pytest.mark.parametrize(
        'filename,is_valid',
        [
            ('first.yml', True),
            ('second.yml', True),
            ('sub.yml', True),
            ('invalid.yml', False),
        ]
    )
    def test_read_file(self, mocker: MockerFixture, filename, is_valid) -> None:
        patch = mocker.patch('flowingo.manager.tasks.pipelines._save_pipelines_to_database')
        if not is_valid:
            with pytest.raises(Exception):
                refresh_pipeline(filename)
        else:
            refresh_pipeline(filename)
            patch.assert_called_once()

            args, kwargs = patch.call_args
            assert len(args) == 1
            assert not kwargs
            pipelines = args[0]
            assert pipelines.keys() == {filename}.union({'sub.yml'})

            for task in pipelines.values():
                assert isinstance(task, dict)

    def test_save_to_database(self, db_session_clear_pipelines: Session) -> None:
        refresh_all_pipelines()
        db_session_clear_pipelines.commit()  # TODO: why session does not update without it?
        db_session_clear_pipelines.begin()

        pipelines = db_session_clear_pipelines.execute(select(Pipeline)).scalars().all()
        assert {i.filename for i in pipelines} == self.PIPELINES

        pipeline_dumps = db_session_clear_pipelines.execute(select(PipelineDump)).scalars().all()
        assert {i.pipeline.filename for i in pipeline_dumps} == self.PIPELINES
        assert {i.id for i in pipelines} == {i.pipeline_id for i in pipeline_dumps}
        assert {i.dump_id for i in pipelines} == {i.id for i in pipeline_dumps}

        pipeline_tags = db_session_clear_pipelines.execute(select(PipelineTag)).scalars().all()
        assert {i.name for i in pipeline_tags} == self.TAG_PIPELINES.keys()

        for tag_name, tag_pipelines in self.TAG_PIPELINES.items():
            pipelines_tags = db_session_clear_pipelines.execute(select(PipelineTag).where(PipelineTag.name == tag_name)).scalars().all()
            assert {i.pipeline.filename for i in pipelines_tags} == tag_pipelines

    def test_delete_file(self, db_session_clear_pipelines: Session, tmp_folder: pathlib.Path) -> None:
        pipelines_folder, conf.pipelines_folder = copy(conf.pipelines_folder), copy(tmp_folder)
        shutil.copy(pipelines_folder / 'sub.yml', tmp_folder / 'sub.yml')

        # Load file
        shutil.copy(pipelines_folder / 'first.yml', tmp_folder / 'current.yml')
        refresh_all_pipelines()

        pipelines = db_session_clear_pipelines.execute(select(Pipeline)).scalars().all()
        assert {i.filename for i in pipelines} == {'current.yml', 'sub.yml'}

        # Delete file
        (tmp_folder / 'current.yml').unlink()
        refresh_all_pipelines()

        pipelines = db_session_clear_pipelines.execute(select(Pipeline)).scalars().all()
        assert {i.filename for i in pipelines} == {'sub.yml'}
        pipeline_dumps = db_session_clear_pipelines.execute(select(PipelineDump)).scalars().all()
        assert {i.pipeline.filename for i in pipeline_dumps} == {'sub.yml'}

    def test_update_file(self, db_session_clear_pipelines: Session, tmp_folder: pathlib.Path) -> None:
        pipelines_folder, conf.pipelines_folder = copy(conf.pipelines_folder), copy(tmp_folder)
        shutil.copy(pipelines_folder / 'sub.yml', tmp_folder / 'sub.yml')

        # Load first file
        shutil.copy(pipelines_folder / 'first.yml', tmp_folder / 'current.yml')
        refresh_all_pipelines()
        db_session_clear_pipelines.commit()  # TODO: why session does not update without it?
        db_session_clear_pipelines.begin()

        pipelines = db_session_clear_pipelines.execute(select(Pipeline)).scalars().all()
        assert {i.filename for i in pipelines} == {'current.yml', 'sub.yml'}
        pipeline_dumps = db_session_clear_pipelines.execute(select(PipelineDump)).scalars().all()
        assert {i.pipeline.filename for i in pipeline_dumps} == {'current.yml', 'sub.yml'}

        # Load second file
        shutil.copy(pipelines_folder / 'second.yml', tmp_folder / 'current.yml')
        refresh_all_pipelines()
        refresh_all_pipelines()
        db_session_clear_pipelines.commit()  # TODO: why session does not update without it?
        db_session_clear_pipelines.begin()

        pipelines = db_session_clear_pipelines.execute(select(Pipeline)).scalars().all()
        assert len(pipelines) == 2
        assert {i.filename for i in pipelines} == {'current.yml', 'sub.yml'}
        pipeline_dumps = db_session_clear_pipelines.execute(select(PipelineDump)).scalars().all()
        assert len(pipeline_dumps) == 3
        assert {i.pipeline.filename for i in pipeline_dumps} == {'current.yml', 'sub.yml'}
