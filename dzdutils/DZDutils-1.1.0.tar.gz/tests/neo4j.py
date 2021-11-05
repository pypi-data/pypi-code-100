import sys
import os
import py2neo
from linetimer import CodeTimer

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))


def test_nodes_to_buckets_distributor():
    from DZDutils.neo4j import nodes_to_buckets_distributor

    base_label = "_TEST_BUCKET_NODE"
    bucket_label_prefix = "_TEST_BUCKET_"
    number_of_nodes = 1000000
    bucket_size = 33333
    bucket_count = 33
    g = py2neo.Graph()

    # TEST BUCKET SIZE

    # clean the plate
    print("Clean old test nodes: ", f"MATCH (n:{base_label}) delete n")
    g.run(f"MATCH (n:{base_label}) delete n")
    print("Create test nodes")
    g.run(f"UNWIND range(1,{number_of_nodes}) as i CREATE (:{base_label})")
    # g.run(f"FOREACH ( i IN range(1,{number_of_nodes}) | CREATE (:{base_label}))")
    with CodeTimer("BucketDistribution", unit="s"):
        print("Start bucket Distribution")
        labels = nodes_to_buckets_distributor(
            g,
            query=f"MATCH (n:{base_label}) return n",
            bucket_size=bucket_size,
            bucket_label_prefix=bucket_label_prefix,
        )
    print("RESULT LABELS", labels)

    # TEST BUCKET COUNT

    # clean the plate
    print("Clean old test nodes: ", f"MATCH (n:{base_label}) delete n")
    g.run(f"MATCH (n:{base_label}) delete n")
    print("Create test nodes")
    g.run(f"UNWIND range(1,{number_of_nodes}) as i CREATE (:{base_label})")

    with CodeTimer("BucketDistribution", unit="s"):
        print("Start bucket Distribution")
        labels = node_to_bucket_distributor(
            g,
            query=f"MATCH (n:{base_label}) return n",
            bucket_count=bucket_count,
            bucket_label_prefix=bucket_label_prefix,
        )
    print("LABEL count", len(labels))
    print("RESULT LABELS", labels)


if __name__ == "__main__":
    test_node_to_bucket_distributor()
