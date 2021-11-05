from typing import List

from enginelib.errors import Error
from enginelib.rds.client import db_client, db_name


def rows_for_cpt(procedure_code: str = '', max_rows: int = 0) -> List:
    """For MPEs, this function does the initial filtering of rows from table multipolicy
    (the MASTER table), returning every row for which the given procedure code appears
    in column {cpt_procedurecode}."""

    clause = f'''WHERE "cpt_procedurecode" = '{procedure_code}' '''  if procedure_code else ''
    limit = f'LIMIT {max_rows}' if max_rows > 0 else ''

    # noinspection SqlResolve
    query = f'''
    SELECT * 
        FROM {db_name}.multipolicy
        {clause}
        {limit};
    '''

    ref_data, err = db_client.GetReferenceData("multi_policy_prefilter", query)
    if err:
        raise Error(f'Not able to access multipolicy reference data set: {err}')
    else:
        ref_data = ref_data or list()
        return [
            {key: str(value) for key, value in row.items()}
            for row in ref_data
        ]
