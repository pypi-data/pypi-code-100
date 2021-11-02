import json
from unittest import mock

from elasticsearch import Elasticsearch

from tests.instrumentation.base import BaseInstrumentorTest


@mock.patch(
    "elasticsearch.connection.http_urllib3.Urllib3HttpConnection.perform_request"
)
class TestElasticsearchoInstrumentor(BaseInstrumentorTest):

    def test_instrumentation(self, request_mock):
        query_result = {
            "took": 9,
            "timed_out": False,
            "_shards": {
                "total": 1,
                "successful": 1,
                "skipped": 0,
                "failed": 0,
            },
            "hits": {
                "total": {"value": 1, "relation": "eq"},
                "max_score": 0.18232156,
                "hits": [
                    {
                        "_index": "test-index",
                        "_type": "doc",
                        "_id": "1",
                        "_score": 0.18232156,
                        "_source": {"name": "tester"},
                    }
                ],
            },
        }

        query_result = json.dumps(query_result)

        request_mock.return_value = (1, {}, query_result)

        es = Elasticsearch()
        es.transport._verified_elasticsearch = True

        search_object = {'query': {'match': {'name': 'tester'}}}
        es.search(index='test-index', body=json.dumps(search_object))

        self.tracer_provider.force_flush()

        spans = self.span_exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)

        elastic_span = spans[0]
        self.assertEqual(
            'opentelemetry.instrumentation.elasticsearch',
            elastic_span.attributes.get('otel.library.name'))

        self.assertEqual('POST', elastic_span.attributes.get('elasticsearch.method'))
        self.assertEqual('/test-index/_search', elastic_span.attributes.get('elasticsearch.url'))
        self.assertEqual(json.dumps(search_object), elastic_span.attributes.get('db.statement'))

        # TODO: uncomment after merging PR in otel-pyton-contrib (https://github.com/open-telemetry/opentelemetry-python-contrib/pull/670)
        # self.assertEqual(query_result, elastic_span.attributes.get('db.query_result'))
