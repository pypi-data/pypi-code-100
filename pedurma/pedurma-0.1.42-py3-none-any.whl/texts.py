import json
import re
from collections import defaultdict
from pathlib import Path

import requests
from openpecha.serializers import HFMLSerializer
from openpecha.utils import download_pecha, load_yaml

from pedurma import config
from pedurma.exceptions import TextMappingNotFound
from pedurma.pecha import NotesPage, Page, PedurmaText, Text
from pedurma.utils import get_pages


def get_text_info(text_id, index):
    texts = index["annotations"]
    for uuid, text in texts.items():
        if text["work_id"] == text_id:
            return (uuid, text)
    return ("", "")


def get_meta_data(pecha_id, text_uuid, meta_data):
    meta = {}
    source_meta = meta_data.get("source_metadata", "")
    if source_meta:
        meta = {
            "work_id": source_meta.get("work_id", ""),
            "img_grp_offset": source_meta.get("img_grp_offset", ""),
            "pref": source_meta.get("pref", ""),
            "pecha_id": pecha_id,
            "text_uuid": text_uuid,
        }
    return meta


def get_hfml_text(opf_path, text_id, index=None):
    serializer = HFMLSerializer(
        opf_path, text_id=text_id, index_layer=index, layers=["Pagination", "Durchen"]
    )
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    return hfml_text


def get_body_text(text_with_durchen):
    body_text = ""
    pages = get_pages(text_with_durchen)
    for page in pages:
        if re.search("<[𰵀-󴉱]?d", page):
            return body_text
        body_text += page
    return body_text


def get_durchen(text_with_durchen):
    durchen = ""
    durchen_start = False
    pages = get_pages(text_with_durchen)
    for page in pages:
        if re.search("<[𰵀-󴉱]?d", page) or durchen_start:
            durchen += page
            durchen_start = True
        if re.search("d>", page):
            return durchen
    if not durchen:
        print("INFO: durchen not found..")
    return durchen


def get_page_id(img_num, pagination_layer):
    paginations = pagination_layer["annotations"]
    for uuid, pagination in paginations.items():
        if pagination["imgnum"] == img_num:
            return (uuid, pagination)
    return ("", "")


def get_link(img_num, vol_meta):
    image_grp_id = vol_meta["image_group_id"]
    link = f"https://iiif.bdrc.io/bdr:{image_grp_id}::{image_grp_id}{int(img_num):04}.jpg/full/max/0/default.jpg"
    return link


def get_note_ref(pagination):
    try:
        return pagination["note_ref"]
    except Exception:
        return ""


def get_clean_page(page):
    pat_list = {
        "page_pattern": r"〔[𰵀-󴉱]?\d+〕",
        "topic_pattern": r"\{([𰵀-󴉱])?\w+\}",
        "start_durchen_pattern": r"\<([𰵀-󴉱])?d",
        "end_durchen_pattern": r"d\>",
        "sub_topic_pattern": r"\{([𰵀-󴉱])?\w+\-\w+\}",
    }
    base_page = page
    for ann, ann_pat in pat_list.items():
        base_page = re.sub(ann_pat, "", base_page)
    base_page = base_page.strip()
    return base_page


def get_page_obj(page, vol_meta, tag, pagination_layer):
    img_num = int(re.search(r"〔[𰵀-󴉱]?(\d+)〕", page).group(1))
    page_id, pagination = get_page_id(img_num, pagination_layer)
    page_content = get_clean_page(page)
    page_link = get_link(img_num, vol_meta)
    note_ref = get_note_ref(pagination)
    if page_content == "":
        page_obj = None
    else:
        if tag == "note":
            page_obj = NotesPage(
                id=page_id,
                page_no=img_num,
                content=page_content,
                name=f"Page {img_num}",
                vol=vol_meta["volume_number"],
                image_link=page_link,
            )
        else:
            page_obj = Page(
                id=page_id,
                page_no=img_num,
                content=page_content,
                name=f"Page {img_num}",
                vol=vol_meta["volume_number"],
                image_link=page_link,
                note_ref=note_ref,
            )

    return page_obj


def get_page_obj_list(text, vol_meta, pagination_layer, tag="text"):
    page_obj_list = []
    pages = get_pages(text)
    for page in pages:
        pg_obj = get_page_obj(page, vol_meta, tag, pagination_layer)
        if pg_obj:
            page_obj_list.append(pg_obj)
    return page_obj_list


def get_vol_meta(vol_num, pecha_meta):
    vol_meta = {}
    vol_num = int(vol_num[1:])
    text_vols = pecha_meta["source_metadata"].get("volumes", {})
    if text_vols:
        for vol_id, vol in text_vols.items():
            if vol["volume_number"] == vol_num:
                vol_meta = vol
    return vol_meta


def construct_text_obj(hfmls, pecha_meta, opf_path):
    pages = []
    notes = []
    for vol_num, hfml_text in hfmls.items():
        vol_meta = get_vol_meta(vol_num, pecha_meta)
        pagination_layer = load_yaml(
            Path(f"{opf_path}/{pecha_meta['id']}.opf/layers/{vol_num}/Pagination.yml")
        )
        durchen = get_durchen(hfml_text)
        body_text = get_body_text(hfml_text)

        pages += get_page_obj_list(body_text, vol_meta, pagination_layer, tag="text")
        if durchen:
            notes += get_page_obj_list(durchen, vol_meta, pagination_layer, tag="note")
    text_obj = Text(id=pecha_meta["text_uuid"], pages=pages, notes=notes)
    return text_obj


def serialize_text_obj(text):
    """Serialize text object to hfml

    Args:
        text (obj): text object

    Returns:
        dict: vol as key and value as hfml
    """
    text_hfml = defaultdict(str)
    pages = text.pages
    notes = text.notes
    for page in pages:
        text_hfml[f"v{int(page.vol):03}"] += f"{page.content}\n\n"
    for note in notes:
        text_hfml[f"v{int(note.vol):03}"] += f"{note.content}\n\n"
    return text_hfml


def get_durchen_page_obj(page, notes):
    for note in notes:
        if note.id == page.note_ref:
            return note
    return None


def get_pecha_paths(text_id, text_mapping=None):
    pecha_paths = {"namsel": None, "google": None}
    if not text_mapping:
        text_mapping = requests.get(config.TEXT_LIST_URL)
        text_mapping = json.loads(text_mapping.text)
    text_info = text_mapping.get(text_id, {})
    if text_info:
        pecha_paths["namsel"] = download_pecha(text_info["namsel"])
        pecha_paths["google"] = download_pecha(text_info["google"])
    else:
        raise TextMappingNotFound
    return pecha_paths


def get_text_obj(pecha_id, text_id, pecha_path=None):
    if not pecha_path:
        pecha_path = download_pecha(pecha_id, needs_update=False)
    pecha_meta = load_yaml(Path(f"{pecha_path}/{pecha_id}.opf/meta.yml"))
    index = load_yaml(Path(f"{pecha_path}/{pecha_id}.opf/index.yml"))
    hfmls = get_hfml_text(f"{pecha_path}/{pecha_id}.opf/", text_id, index)
    text_uuid, text = get_text_info(text_id, index)
    pecha_meta["text_uuid"] = text_uuid
    text = construct_text_obj(hfmls, pecha_meta, pecha_path)
    return text


def get_pedurma_text_obj(text_id, pecha_paths=None):
    if not pecha_paths:
        pecha_paths = get_pecha_paths(text_id)
    text = {}
    for pecha_src, pecha_path in pecha_paths.items():
        pecha_id = Path(pecha_path).stem
        text[pecha_src] = get_text_obj(pecha_id, text_id, pecha_path)
    pedurma_text = PedurmaText(
        text_id=text_id, namsel=text["namsel"], google=text["google"]
    )
    return pedurma_text
