# coding=utf-8
from typing import List

from sklearn import neighbors
import tensorflow as tf
import tensorflow_hub as hub
import tf_sentencepiece  # Not used directly but needed to import TF ops.
from simpleneighbors import SimpleNeighbors
from tensorflow.python import global_variables_initializer, tables_initializer, Session
from tensorflow.python.keras.backend import placeholder

from mammut.common.package import Package

import logging

log = logging.getLogger(__name__)


class Paraphrases:
    NUM_RESULTS = 10

    def __init__(self, package: Package):
        self.package = package
        module_url = (
            "https://tfhub.dev/google/universal-sentence-encoder-multilingual/1"
        )
        # Set up graph.
        g = tf.Graph()
        with g.as_default():
            self.text_input = placeholder(dtype=tf.string, shape=[None])
            multiling_embed = hub.Module(module_url)
            self.embedded_text = multiling_embed(self.text_input)
            init_op = tf.group([global_variables_initializer(), tables_initializer()])
        g.finalize()
        # Initialize session.
        self.session = Session(graph=g)
        self.session.run(init_op)
        self.indexes = {}

    def get_similar_phrases(
        self, corpus_name: str, corpus_type: str, query: str
    ) -> List[str]:
        """Look in a corpus for all phrases similar to one provided.

        :param corpus_name: Name of the corpus to check.
        :param corpus_type: Type of the corpus to check.
        :param query: Phrase which we are looking similarities for.
        :return: List of Phrases found in the corpus specified.
        """
        index_by_corpus_name = {}
        if corpus_type in self.indexes:
            index_by_corpus_name = self.indexes[corpus_type]
        else:
            self.indexes[corpus_type] = index_by_corpus_name
        index = None
        if corpus_name in index_by_corpus_name:
            index = index_by_corpus_name[corpus_name]
        else:
            corpus = self.package.corpus_map.get_corpus(corpus_type, corpus_name)
            all_events = [
                tm.original_text
                for s in corpus.sceneries.values()
                for e in s.events
                for tm in e.tokenized_messages
            ]
            events_embeddings = self.session.run(
                self.embedded_text, feed_dict={self.text_input: all_events}
            )
            num_index_trees = 40
            embedding_dimensions = len(events_embeddings[0])
            metric = None
            metrics = ["dot", "cosine", "euclidean"]
            for m in metrics:
                if m in neighbors.VALID_METRICS["brute"]:
                    metric = m
                    break
            if not metric:
                raise RuntimeError("None of the valid metrics were found in sklearn.")
            index = SimpleNeighbors(embedding_dimensions, metric=metric)
            for i in range(len(all_events)):
                index.add_one(all_events[i], events_embeddings[i])
            index.build(n=num_index_trees)
        query_embedding = self.session.run(
            self.embedded_text, feed_dict={self.text_input: [query]}
        )[0]
        search_results = index.nearest(query_embedding, n=Paraphrases.NUM_RESULTS)
        return search_results
