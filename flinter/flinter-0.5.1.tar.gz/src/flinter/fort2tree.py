"""Scan a folder for fortran files and build the tree."""

import os
import glob
import yaml
from ctypes import c_int64
import tkinter as tk

from nobvisual import tkcirclify
from nobvisual.utils import path_as_str
from nobvisual.helpers import from_nested_struct_to_nobvisual

from flinter.initialize import init_languages_specs, rate
from flinter.struct_analysis import scan_fortran_file


__all__ = ["dumpstats", "score_cli"]


def dumpstats(wdir, fname, flinter_rc=None):
    """Dump score stats in a yaml file"""

    scantree = fort2tree(wdir, flinter_rc)

    with open(fname, "w") as fout:
        yaml.dump(scantree, fout)


def score_cli(wdir, flinter_rc=None, max_lvl=None):
    """Show stats in terminal"""

    scantree = fort2tree(wdir, flinter_rc)

    if max_lvl == 0:
        rating = '{:.2f}'.format(scantree['rate'])
        size = scantree['size']
        print(f"Flinter global rating -->|{rating}|<--  ({size} statements)")
        return

    head = "  {:<3} {:<50} {:<10} {:<10}".format("lvl", "path", "rate", "size (stmt)")
    print(head)

    indent = "........"

    def _rec_print(data, lvl=0):

        # head = str()
        # head +=f"{indent(lvl, char='-')}{data['path']}"
        # head += f" rate : {'{:.2f}'.format(data['rate'])}"
        # head += f" size : {data['size']} statements"

        head = "  {:<3} {:<50} {:<10} {:<10}".format(lvl, data['path'], '{:.2f}'.format(data['rate']), data['size'])

        print(head)
        if "regexp_rules" in data:
            for key in data["regexp_rules"]:
                print(f"{indent} {key} :  {str(data['regexp_rules'][key])}")
        if "struct_rules" in data:
            for key in data["struct_rules"]:
                print(f"{indent} {key} :  {'/'.join(data['struct_rules'][key])}")

        if data["children"]:
            if lvl >= max_lvl:
                print(f"{indent}.")
                return
            else:
                for child in data["children"]:
                    _rec_print(child, lvl=lvl + 1)
    _rec_print(scantree)


def visualfort(wdir, flinter_rc=None, minrate=-10, norate=False,
               start_mainloop=True):
    """Visualization os fortran source code
    """
    scantree = fort2tree(wdir, flinter_rc)
    nstruct = tree2circ(scantree, minrate=minrate, norate=norate)

    circles = from_nested_struct_to_nobvisual(nstruct)

    if norate:
        colorscale = None
    else:
        colorscale = ("Standard compliance", "High (10)", f"Low ({str(minrate)})")

    draw_canvas = tkcirclify(
        circles,
        color="#eeeeee",
        colorscale=colorscale,
        title=f"Flinter showing {str(wdir)}",
    )

    draw_canvas.show_names(level=2)

    if start_mainloop:
        tk.mainloop()


def fort2tree(wdir, flinter_rc=None):
    """ Build the structure of a folder tree.

    :params wdir: path to a directory
    """

    rule_sets = init_languages_specs(flinter_rc)

    def _rec_subitems(path):
        name = os.path.split(path)[-1]
        out = {
            "name": name,
            "path": path,
            "size": 0,
            "struct_nberr": 0,
            "regexp_nberr": 0,
            "rate": 0,
            "children": list()
        }
        if os.path.isfile(path):
            rules = rule_sets.get_from_fname(path)
            if rules:
                try:
                    with open(path, "r", encoding="utf8") as fin:
                        out = scan_fortran_file(path, fin.read(), rules)
                        # for block in out["children"]:
                        #    out["size"]+= block["size"]
                        #    out["struct_nberr"]+= block["struct_nberr"]
                        #    out["regexp_nberr"]+= block["regexp_nberr"]
                        # out["rate"] = rate(
                        #    out["size"], out["struct_nberr"], out["regexp_nberr"]
                        #)
                except UnicodeDecodeError:
                    print(f"File {path} is not encoded in UTF-8")
                except ValueError:
                    print(f"No lizard reader for file \"{path}\"")
            else:
                print(f"No rule file found for file \"{path}\"")

        else:
            out["children"] = list()
            paths = glob.glob(os.path.join(path, "**"))
            for nexpath in paths:
                record = _rec_subitems(nexpath)
                if record["size"] > 0:
                    out["children"].append(record)

                    out["size"] += record["size"]
                    out["struct_nberr"] += record["struct_nberr"]
                    out["regexp_nberr"] += record["regexp_nberr"]

            out["rate"] = rate(
                out["size"], out["struct_nberr"], out["regexp_nberr"]
            )

        return out
    out = _rec_subitems(os.path.relpath(wdir))

    return out


def tree2circ(tree, minrate=-20, norate=False, item_id=c_int64(-1)):
    """Translate the tree structure to a circlify object"""

    def _rec_tree2circ(subtree, item_id):
        # TODO: normalize paths?
        path_ls = subtree["path"].split("/")
        text = path_as_str(path_ls)

        item_id.value += 1
        out = {
            "id": item_id.value,
            "datum": max(1, subtree["size"]),
            "children": list(),
            "name": path_ls[-1],
            "text": text,
        }

        for childtree in subtree["children"]:
            out["children"].append(_rec_tree2circ(childtree, item_id))

        if norate:
            pass
        else:
            try:
                value = max((10 - subtree["rate"]) / (10. - minrate), 0)
                out["text"] += f"\n rate {subtree['rate']:.2f}"
                out["color"] = f"colormap: {value}"
            except KeyError:
                out["color"] = "#ff0000"
        return out

    out = [_rec_tree2circ(tree, item_id)]
    return out
