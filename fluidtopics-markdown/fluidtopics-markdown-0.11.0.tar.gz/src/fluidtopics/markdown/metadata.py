import logging
import re
from pathlib import Path

from typing import Tuple, Dict, TextIO
from io import StringIO
from enum import Enum
import yaml

from fluidtopics.connector.model.metadata import SemanticMetadata


class MetadataError(Exception):
    pass


logger = logging.getLogger("fluidtopics.markdown")

RE_LINEMETA = re.compile(r'\s*\[_metadata_\:(\w*[\:\w*]*)\]\:\s*-\s*["\'](.+)["\']')
RE_YAMLMETA_BEGIN = re.compile(r'^---')
RE_YAMLMETA_END = re.compile(r'^---|^\.\.\.')
RE_H1_MD = re.compile("^# (.*)$")


class MetadataType(Enum):
    NoMeta = 1
    LineMeta = 2
    YamlMeta = 3

# List of meta data that ought to be single-valued
# See: https://doc.antidot.net/r/FT/3.7/empower-metadata/Metadata-in-Fluid-Topics/Semantic-Metadata


# The authorized single value semantic meta are given
# by the official fluidtopics API
# see: https://pypi.org/project/fluidtopics
FT_SEMANTIC_META = SemanticMetadata.ALL
# This one is authorized too for md2ft
FT_ORIGIN_ID = "ft:originID"
FT_LANG = "ft:lang"
FT_SEMANTIC_META.add(FT_ORIGIN_ID)
FT_SEMANTIC_META.add(FT_LANG)
SINGLE_VALUE_M2FT = {"audience"}

SINGLE_VALUE_META = SINGLE_VALUE_M2FT.union(FT_SEMANTIC_META)


def _detect_metadata(f: Path) -> MetadataType:
    """Detects which kind of markdown metadata is present in markdown file (if any)
    Metadata should be present on the very first line. If there is no metadata
    marker on the first line, it is assumed that there is no metadata in the file.
    """
    metatype = MetadataType.NoMeta
    with f.open('r') as mdfile:
        firstline = mdfile.readline()
        if RE_YAMLMETA_BEGIN.match(firstline):
            metatype = MetadataType.YamlMeta
        elif RE_LINEMETA.match(firstline):
            metatype = MetadataType.LineMeta
    return metatype


def _get_title_from_md_h1(line: str, metas: Dict[str, str]) -> bool:
    match_h1 = RE_H1_MD.match(line)
    if match_h1:
        metas[SemanticMetadata.TITLE] = match_h1.group(1)
        return True
    return False


def _read_yaml_metas(mdfile: TextIO, md_content: StringIO) -> Tuple[Dict[str, str], str, int]:
    metas = {}
    # skip first line which should be the YAML data begin marker
    _ = mdfile.readline()
    yamldata = StringIO()
    buffer = yamldata
    end_marker = False
    title_in_meta = False
    h1_count = 0
    for k, line in enumerate(mdfile.readlines()):
        if RE_YAMLMETA_END.match(line):
            metas.update(yaml.safe_load(yamldata.getvalue()))
            title_in_meta = SemanticMetadata.TITLE in metas
            buffer = md_content
            end_marker = True
            continue
        if not title_in_meta and _get_title_from_md_h1(line, metas):
            h1_count += 1
        else:
            buffer.write(line)
    if not end_marker:
        raise MetadataError("No yaml metadata end marker found ??")
    return metas, md_content, h1_count


def _read_legacy_metas(mdfile: TextIO, md_content: StringIO) -> Tuple[Dict[str, str], str, int]:
    metas = {}
    h1_count = 0
    for line in mdfile:
        m = RE_LINEMETA.match(line)
        if m:
            key, value = (m.group(1), m.group(2))
            # case insensitivity title compatibility
            if key.lower() == "title":
                metas["title"] = value
            else:
                # create a multi-valued meta, from list of repeated meta
                if key in metas:
                    if type(metas[key]) == list:
                        metas[key].append(value)
                    else:
                        metas[key] = [metas[key], value]
                else:
                    metas[key] = value
        else:
            if _get_title_from_md_h1(line, metas):
                h1_count += 1
                continue
            md_content.write(line)
    return metas, md_content, h1_count


def get_md_metas(f: Path, implicit_meta: bool = False) -> Tuple[Dict[str, str], str]:
    """Get markdown metadata from a file and verify other MD content is there too"""
    metatype = _detect_metadata(f)
    # at the end the md_content will contain the md data with the metadata stripped-out
    md_content = StringIO()
    h1_count = 0

    logger.debug(f"MD file={f}, MetadataType={metatype}")
    with f.open('r') as mdfile:
        if metatype == MetadataType.LineMeta:
            metas, md_content, h1_count = _read_legacy_metas(mdfile, md_content)
        elif metatype == MetadataType.YamlMeta:
            metas, md_content, h1_count = _read_yaml_metas(mdfile, md_content)
        elif metatype == MetadataType.NoMeta:
            # when no meta is present in file we should at least
            # handle H1 header as ft:title.
            metas = {}
            for line in mdfile:
                if _get_title_from_md_h1(line, metas):
                    h1_count += 1
                else:
                    md_content.write(line)

    if h1_count > 1:
        raise MetadataError("No ft:title meta and several H1 in content unsupported")

    metas = _handle_implicit_and_legacy_metas(metas, f,
                                              metatype, implicit_meta)
    metas = _check_multivalued_metas(metas, f)
    return metas, md_content.getvalue()


def _handle_implicit_and_legacy_metas(metas: Dict[str, str],
                                      f: Path,
                                      metatype: MetadataType,
                                      implicit_meta: bool) -> Dict[str, str]:
    logger.debug(f"metatype={metatype}, metas={metas}")
    # Handle implicit meta and compatibility
    if not metas and implicit_meta:
        metas = {SemanticMetadata.TITLE: f.stem}
    # Handle meta compatibility format
    if SemanticMetadata.TITLE not in metas and "title" in metas:
        logger.warning("Using '[_metadata_:title]:-' for title is deprecated")
        logger.warning("Use '[_metadata_:ft:title]:- \"your title\"'")
        metas[SemanticMetadata.TITLE] = metas["title"]
        del metas["title"]
    if "FT_ORIGIN_ID" not in metas and "originID" in metas:
        logger.warning("Using '[_metadata_:originID]:-' for originID is deprecated")
        logger.warning("Use '[_metadata_:ft:originID]:- \"your originID\"'")
        metas["FT_ORIGIN_ID"] = metas["originID"]
        del metas["originID"]
    return metas


def _check_multivalued_metas(metas: Dict[str, str], f) -> Dict[str, str]:
    # Check that ft semantic metadata are in the list of authorized meta
    # and that some meta are not multivalued
    for k, v in metas.items():
        if (type(v) == list):
            if len(v) == 0:
                raise MetadataError(f"meta {k} is an array with no value (in file {f})")
            elif len(v) == 1:
                # replace list with a single value
                metas[k] = v[0]
        logger.debug(f"Check meta {k} with value {v} (type={type(v)})")
        if k.startswith("ft:") and k not in FT_SEMANTIC_META:
            raise MetadataError(f"Fluid Topics Semantic meta {k} cannot be set (value = {v} in file {f})")
        if (k in SINGLE_VALUE_META) and (type(v) == list) and len(v) > 1:
            raise MetadataError(f"meta {k} cannot be multi-valued (current = {v} in file {f})")
    return metas
