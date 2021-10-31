from copy import copy

import pytest
from pytest_mock import MockerFixture
from sqlalchemy import select

from flowingo.manager.tasks.pipelines import refresh_all_pipelines, refresh_all_tasks, refresh_pipeline
from flowingo.manager.tasks.runtime import (
    end_pipeline_run_task,
    if_task,
    merge_context_task,
    run_pipeline,
    run_sub_pipeline_task,
    start_pipeline_run_task,
)
from flowingo.models import Pipeline, PipelineDump, PipelineTag, Session, Task, TaskGroup, TaskTag


@pytest.mark.usefixtures("config_folders")
class TestTasks:
    class _Signature:
        def replace(self, args=None, kwargs=None):
            return self

    TEST_CONTEXT = {'a': 1, 'b': 2}

    @pytest.mark.parametrize(
        'contexts,merged_context',
        [
            ([{}], {}),
            ([{'a': 12}, None], {'a': 12}),
            ([None, {'a': 12}], {'a': 12}),
            ([{'a': 12}, {1: None}, {1: None}], {'a': 12, 1: None}),
            ([{'a': 12}, {'b': 13}, {'b': 13}], {'a': 12, 'b': 13}),
        ]
    )
    def test_merge_context(self, contexts: list, merged_context: dict):
        context = merge_context_task(contexts)
        assert context == merged_context

    @pytest.mark.parametrize(
        'context,key,values',
        [
            ({'a': 'a'}, 'a', {'a': 'filename.yml'}),
            ({'a': 'a'}, 'a', {'a': ['tasks here']}),
            ({'a': 'a'}, 'a', {'default': ['tasks here']}),
            ({'a': 'a'}, 'a', {}),
        ]
    )
    def test_if(self, mocker: MockerFixture, context, key, values):
        signature = self._Signature()
        patch_get_chain_task = mocker.patch('flowingo.manager.tasks.runtime._get_chain_task', return_value=signature)
        patch_start_pipeline_run_task_s = mocker.patch.object(start_pipeline_run_task, 's', return_value=signature)
        patch_if_task_replace = mocker.patch.object(if_task, 'replace', return_value=context)

        assert if_task(context, key=key, values=values) == context

        if values:
            assert patch_get_chain_task.call_count + patch_start_pipeline_run_task_s.call_count == 1
            patch_if_task_replace.assert_called_once()

    def test_run_sub_pipeline(self, mocker: MockerFixture, db_session_clear_pipelines: Session) -> None:
        context = copy(self.TEST_CONTEXT)

        refresh_all_pipelines()
        db_session_clear_pipelines.commit()  # TODO: why session does not update without it?
        db_session_clear_pipelines.begin()

        pipeline = db_session_clear_pipelines.execute(select(Pipeline)).scalar()

        signature = self._Signature()
        patch_get_chain_task = mocker.patch('flowingo.manager.tasks.runtime._get_chain_task', return_value=signature)
        patch_run_sub_pipeline_task_replace = mocker.patch.object(run_sub_pipeline_task, 'replace', return_value=context)

        # Test sub pipeline no id
        with pytest.raises(RuntimeError):
            run_sub_pipeline_task(context, pipeline_id=100000)

        # Test sub pipeline by id
        assert run_sub_pipeline_task(context, pipeline_id=pipeline.id) == self.TEST_CONTEXT
        patch_get_chain_task.assert_called_once()
        patch_get_chain_task.call_args = (pipeline.tasks,)
        patch_run_sub_pipeline_task_replace.assert_called_once()

        patch_get_chain_task.call_count, patch_run_sub_pipeline_task_replace.call_count = 0, 0

        # Test sub pipeline no filename
        with pytest.raises(RuntimeError):
            run_sub_pipeline_task(context, pipeline_filename='wrong_filename.yaml')

        # Test sub pipeline by filename
        assert run_sub_pipeline_task(context, pipeline_filename=pipeline.filename) == context
        patch_get_chain_task.assert_called_once()
        patch_get_chain_task.call_args = (pipeline.tasks,)
        patch_run_sub_pipeline_task_replace.assert_called_once()

        # Test not provided anything
        with pytest.raises(RuntimeError):
            run_sub_pipeline_task(context)

    def test_start_pipeline_run(self, mocker: MockerFixture, db_session_clear_pipelines: Session) -> None:
        # context = copy(self.TEST_CONTEXT)
        pass

    def test_end_pipeline_run(self, mocker: MockerFixture, db_session_clear_pipelines: Session) -> None:
        # context = copy(self.TEST_CONTEXT)
        pass


class TestPipelines:
    pass
