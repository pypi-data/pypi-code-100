#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
from ldict.lazyval import LazyVal


def cached(d, cache):
    def closure(outputf, id, ids, data, output_fields):

        def func(**kwargs):
            # Try loading.
            if id in cache:
                return cache[id]

            # Process and save (all fields, to avoid a parcial ldict being stored).
            result = k = None
            for k, fid in ids.items():
                # TODO: all lazies are evaluated, but show() still shows deps as lazy.
                #    Fortunately the dep is evaluated only once.
                if isinstance(data[k], LazyVal):
                    data[k] = data[k](**kwargs)
                cache[fid] = data[k]
                if k == outputf:
                    result = data[k]
            if result is None:
                if k is None:
                    raise Exception(f"No ids")
                raise Exception(f"{k=} not in output fields: {output_fields}. ids: {ids.items()}")

            # Return requested value.
            return result

        return func

    data = d.data.copy()
    lazies = False
    output_fields = []
    for field, v in list(data.items())[:-2]:
        if isinstance(v, LazyVal):
            output_fields.append(field)
            lazies = True
            id = d.hashes[field].id if field in d.hashes else d.hoshes[field].id
            deps = {"^": None}
            deps.update(v.deps)
            lazy = LazyVal(field, closure(field, id, d.ids, d.data, output_fields), deps, None)
            data[field] = lazy

    # Eager saving when there are no lazies.
    if not lazies:
        for k, v in list(data.items())[:-2]:
            if k not in cache:
                cache[k] = data[k]

    return d.clone(data)
