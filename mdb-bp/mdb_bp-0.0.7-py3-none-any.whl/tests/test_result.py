from mdb_bp import result


def test_exec_result_basics():
    res = result.result(10, 3)

    assert res.affected_rows == 10, "incorrect affected rows"
    assert res.insert_id == 3, "incorrect insert id"
