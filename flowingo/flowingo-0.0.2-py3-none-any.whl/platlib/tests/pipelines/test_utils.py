import pytest

from flowingo.pipelines.utils import HASH_LEN, get_pipeline_hash, get_pipeline_tasks_hash


class TestHash:
    def test_hash_len(self):
        assert len(get_pipeline_hash({'tasks': '1'})) == HASH_LEN

    @pytest.mark.parametrize(
        'tasks',
        [[], ['string'], [False, 'string'], [''], [[12], {'d': 12, 'c': []}], [None], [42], [42.42]]
    )
    def test_inner_types(self, tasks):
        pipeline = {'tasks': tasks}
        hash_str = get_pipeline_hash(pipeline)
        assert hash_str != ''

    def test_not_only_tasks_hashed(self):
        hash_str_1 = get_pipeline_hash({'title': 'title', 'tasks': [1, 2, 3]})
        hash_str_2 = get_pipeline_hash({'title': 'other', 'tasks': [1, 2, 3]})
        assert hash_str_1 != hash_str_2

    def test_only_tasks_hashed(self):
        hash_str_1 = get_pipeline_tasks_hash([{'a': 1}, {'a': 2}, {'a': 3}])
        hash_str_2 = get_pipeline_tasks_hash([{'a': 1}, {'a': 2}, {'a': 3}])
        assert hash_str_1 == hash_str_2

        hash_str_3 = get_pipeline_tasks_hash([{'a': 2}, {'a': 1}, {'a': 3}])
        assert hash_str_1 != hash_str_3
