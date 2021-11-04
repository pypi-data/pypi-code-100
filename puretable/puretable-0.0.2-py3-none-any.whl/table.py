'''
This is a kind of table that stores arbitrary objects with a primary key,
and allows to select them by matching the specified fields.

Perhaps it could be replaced by lightweight in-memory RDBMS, e.g. SQLite.
'''
import logging

from typing import Any, Optional, Set, Tuple, Iterator, Union

Addable = Union[int, float, complex]


__all__ = (
    'Table',
)


class Table:
    def __init__(self,
                 records_class=None,
                 primary_key='id',
                 subscriptable: bool = False,
                 indices: Optional[Set[str]] = None,
                 sums: Optional[Set[Tuple[str, str]]] = None,
                 warn_ineffectiveness: bool = False,
                 # unique: Optional[Dict] = None,
                 ):

        self._records_class = records_class  # Just for information
        self._subscriptable = subscriptable  # Content dicts, otherwise objects
        self._warn_ineffectiveness = warn_ineffectiveness

        # Data definition
        if indices is None:
            self._desc_indices = set()
        else:
            self._desc_indices = set(indices)

        if sums is None:
            self._desc_sums = set()
        else:
            self._desc_sums = set(sums)

        # Function to get primary key
        if callable(primary_key):
            self._pkf = primary_key
        elif isinstance(primary_key, str):
            if self._subscriptable:
                self._pkf = lambda rec: rec.get(primary_key)
            else:
                self._pkf = lambda rec: getattr(rec, primary_key)
        else:
            raise ValueError('Unknown primary key getter')

        self._init_structures()

    def _init_structures(self):
        self._recs = dict()

        # List of fields which must be indexed
        self._indx = dict()
        for field_name in self._desc_indices:
            self._indx[field_name] = dict()

        # List of fields which must be summarized
        self._sums = dict()
        for addend_name, condvar in self._desc_sums:
            if addend_name not in self._sums:
                self._sums[addend_name] = dict()
            self._sums[addend_name][condvar] = dict()

    def _get_field_value(self, rec, field_name):
        if self._subscriptable:
            return rec.get(field_name, None)
        else:
            return getattr(rec, field_name)

    def __len__(self) -> int:
        return len(self._recs)

    def _warn(self, msg: str):
        if self._warn_ineffectiveness:
            logging.warning('Table: ' + msg)

    def drop(self):
        '''Clears the table entirely'''
        self._init_structures()

    def upsert(self, rec):
        pk = self._pkf(rec)
        self._recs[pk] = rec

        # Add to index
        for k in self._indx:
            val = self._get_field_value(rec, k)
            if val not in self._indx[k]:
                self._indx[k][val] = set()
            self._indx[k][val].add(pk)

        # Add to sums
        for term_name in self._sums:
            term_val = self._get_field_value(rec, term_name)
            for facet_name in self._sums[term_name]:
                facet_val = self._get_field_value(rec, facet_name)

                if facet_val not in self._sums[term_name][facet_name]:
                    self._sums[term_name][facet_name][facet_val] = 0
                self._sums[term_name][facet_name][facet_val] += term_val

    def remove_by_key(self, key) -> bool:
        '''Returns true if the record was existed and was actually deleted'''
        if key in self._recs:
            rec = self._recs[key]

            # Remove from index
            for k in self._indx:
                val = self._get_field_value(rec, k)
                self._indx[k][val].discard(key)
                if not self._indx[k][val]:
                    del self._indx[k][val]

            # Subtract from sums
            for term_name in self._sums:
                term_val = self._get_field_value(rec, term_name)
                for facet_name in self._sums[term_name]:
                    facet_val = self._get_field_value(rec, facet_name)
                    self._sums[term_name][facet_name][facet_val] -= term_val

            del self._recs[key]
            return True
        else:
            return False

    def remove_object(self, rec) -> bool:
        '''Remove the single record, returns true if record was existed'''
        return self.remove_by_key(self._pkf(rec))

    def remove(self, query=None) -> int:
        '''Removes objects, returns number of removed'''
        keys = self.select_keys(query)
        n = 0
        for key in keys:
            if self.remove_by_key(key):
                n += 1
        return n

    def exists_by_key(self, key) -> bool:
        '''Returns true if key is known'''
        return key in self._recs

    def exists(self, rec) -> bool:
        '''Returns true if record is known'''
        return self._pkf(rec) in self._recs

    # def select_keys_naive(self, query=None) -> Set[Any]:
    #     '''Returns set of primary keys'''
    #
    #     if query is None:
    #         found = set(self._recs.keys())
    #     else:
    #         found = set()
    #
    #         def match(obj):
    #             peer = True
    #             for field in query:
    #                 if self._get_field_value(obj, field) != query[field]:
    #                     peer = False
    #                     break
    #             return peer
    #
    #         for k, v in self._recs.items():
    #             if match(v):
    #                 found.add(k)
    #
    #     return found

    def select_keys(self, query=None) -> Set[Any]:
        '''Returns set of primary keys'''
        found = set()

        if query is None or not query:
            self._warn(f'Fullscan due to empty query')
            found = set(self._recs.keys())
        else:
            empty_from_index = False
            is_indexed = set()
            not_indexed = set()
            for k, v in query.items():
                if k in self._indx:
                    is_indexed.add(k)
                    if v in self._indx[k]:
                        # There're records with k=v
                        got = self._indx[k][v]

                        if len(is_indexed) > 1:
                            # Not first indexed field, intersect with previous
                            found &= got
                        else:
                            found = got.copy()

                        if not found:
                            # Intersection is an empty set
                            empty_from_index = True
                            break
                    else:
                        # No records with k=v at all
                        empty_from_index = True
                        break
                else:
                    not_indexed.add(k)

            if empty_from_index:
                # Nothing found
                found = set()
            elif not_indexed:
                # Found something, but we still need to filter
                self._warn(f'Query fields are not covered by index: {not_indexed!r}')

                def match(obj):
                    peer = True
                    for field in not_indexed:
                        if self._get_field_value(obj, field) != query[field]:
                            peer = False
                            break
                    return peer

                # Fetch records from found that satisfy the rest of the query
                filtered = set()
                if found:
                    samples = found
                else:
                    # There were no indexed fields, is_indexed is empty
                    samples = set(self._recs.keys())
                for k in samples:
                    if match(self._recs[k]):
                        filtered.add(k)
                found = filtered
            else:
                # Query is full covered by indices
                # found = found
                pass

        return found

    def select(self, query=None) -> Iterator[Any]:
        '''Returns generator, which returns records'''
        for key in self.select_keys(query):
            yield self._recs[key]

    def select_one_by_key(self, key):
        '''Returns one record by its primary key'''
        return self._recs.get(key, None)

    def select_one(self, query=None):
        '''Returns only first record'''
        for rec in self.select(query):
            return rec

    def count(self, query=None) -> int:
        return len(self.select_keys(query))

    def distinct(self, field, query=None) -> Set[Any]:
        '''Returns distinct values of field'''
        res = set()

        if field in self._indx and (query is None or not query):
            res = set(self._indx[field].keys())
        else:
            for rec in self.select(query):
                res.add(self._get_field_value(rec, field))

        return res

    def _precalculated_sum(self, field, condvar, condvalue):
        s = None
        if field in self._sums:
            if condvar in self._sums[field]:
                if condvalue in self._sums[field][condvar]:
                    s = self._sums[field][condvar][condvalue]
                else:
                    s = 0
        return s

    def sum(self, field, query=None) -> Addable:
        '''Returns sum of values of field'''
        s = None

        if len(query) == 1:
            condvar = list(query.keys())[0]
            condvalue = query[condvar]
            s = self._precalculated_sum(field, condvar, condvalue)

        if s is None:
            self._warn(f'Calculating the sum of {field} by iteration, '
                       f'query is {query!r}')
            s = 0
            for rec in self.select(query):
                s += self._get_field_value(rec, field)

        return s
