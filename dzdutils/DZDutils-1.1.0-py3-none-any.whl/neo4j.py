import time
import py2neo
import re
import math
from typing import Callable, Dict, List


def wait_for_db_boot(neo4j: Dict = {}, timeout_sec=120, log_func: Callable = print):
    """[summary]

    Args:
        neo4j (Dict, optional): py2neo.Graph() properties as dict. Defaults to {}.
        timeout_sec (int, optional): How long do we want to wait in seconds. Defaults to 120.

    Raises:
        TimeoutError: [description]
    """

    timeout = time.time() + timeout_sec
    last_exception = None
    db_runs = False
    log_func(f"Waiting {timeout_sec} seconds for neo4j@'{neo4j}' to boot up.")
    while not db_runs:
        try:
            g = py2neo.Graph(**neo4j)
            g.run("MATCH (n) RETURN n limit 1")
            log_func("Neo4j booted")
            db_runs = True
        except Exception as e:
            last_exception = e
            log_func(".")
            time.sleep(5)
        if time.time() > timeout:
            log_func(f"...neo4j@'{neo4j}' not booting up.")
            raise last_exception


def nodes_to_buckets_distributor(
    graph: py2neo.Graph,
    query: str,
    bucket_size: int = None,
    bucket_count: int = None,
    bucket_label_prefix: str = "BucketNo",
):
    """Supply a query returning nodes. These nodes will be distributed into sequences labels ("buckets")

    Args:
        graph (py2neo.Graph): [description]
        query (str): A query that is returning any node. The return param MUST be called `n` .e.g `Match (n:Person) return n`
        bucket_size (int, optional): Nodes per bucket. You will get a variable number of buckets of a fixed size
        bucket_count (int, optional): Counts of buckets; you will get a fixed number of buckets with a variable amount of nodes based on your query
        bucket_label_prefix (str, optional): [description]. Defaults to "BucketNo".
    Returns:
        [lst[str]]: Returns a list of str containing the generated label names
    """
    if bucket_size and bucket_count:
        raise ValueError(
            f"You can only set `bucket_size` or `bucket_count`. Not both at the same time. Got `bucket_size={bucket_size}` and `bucket_count={bucket_count}`"
        )
    elif bucket_count is None and bucket_size is None:
        raise ValueError(
            f"You have to set set `bucket_size` or `bucket_count`. Both are None at the moment."
        )
    if graph is None:
        graph = py2neo.Graph()
    node_count = 0
    if bucket_count:
        node_count = graph.run(
            f"CALL {{{query}}} return count(n) as cnt"
        ).to_data_frame()["cnt"][0]
        bucket_size = math.ceil(node_count / bucket_count)
        if bucket_size < 1:
            bucket_size = 1

    if bucket_size:
        iter_query: str = f"""
            CALL apoc.periodic.iterate(
            "CALL {{{query}}}
            WITH apoc.coll.partition(collect(n),{bucket_size}) as bucket_list
            WITH bucket_list, range(0, size(bucket_list)) AS bucket_count
            UNWIND bucket_count AS i
            return bucket_list[i] as bucket, i",
            "UNWIND bucket as n CALL apoc.create.addLabels(n,['{bucket_label_prefix}' + i]) YIELD node return count(*)",
            {{batchSize:1, parallel:true}})
            """
        res = graph.run(iter_query)

        if res.to_data_frame()["failedOperations"][0] != 0:
            raise ValueError(f"Bucketing failed: Cyper error message:\n{res}")
    # find and return the bucket labels.
    # todo: this is dirty. better would be to catch the return labels directly from the periodic query which is creating the labels. dk if possible atm
    labels = (
        graph.run(
            f'CALL db.labels() YIELD label WHERE label STARTS WITH "{bucket_label_prefix}" RETURN label'
        )
        .to_data_frame()
        .values.tolist()
    )

    match = re.compile(f"^{bucket_label_prefix}([0-9]*)$")
    return [
        label for label_list in labels for label in label_list if match.match(label)
    ]
