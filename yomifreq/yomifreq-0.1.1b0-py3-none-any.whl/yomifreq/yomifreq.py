import argparse
import json
import regex as re
import zipfile
from collections import defaultdict
from itertools import chain
from typing import List

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from sudachipy import tokenizer
from sudachipy import dictionary
from tqdm import tqdm

CJK_PATTERN = re.compile(r"([\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+)", re.UNICODE)
SPLIT_MODES = [tokenizer.Tokenizer.SplitMode.B, ]
Tokenizer = dictionary.Dictionary(dict_type="full").create()


def book_strings(book: ebooklib.epub.EpubBook):
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        for strings in filter_soup_to_strings(BeautifulSoup(doc.get_content(), features="lxml")):
            yield strings


def books_strings(books: List[ebooklib.epub.EpubBook]):
    return tqdm(chain(*(book_strings(b) for b in books)))


def derubify(tree):
    rubys = tree.find_all("ruby")
    for ruby in rubys:
        _ruby = "".join([word.string for word in ruby.find_all("rb")])
        ruby.replace_with(_ruby)
    return tree


def remove_spans(tree):
    """Conversion with Calibre leaves useless <span> sections, which this function removes"""
    spans = tree.find_all("span")
    for span in spans:
        span.unwrap()
    return tree


def filter_soup_to_strings(tree):
    remove_spans(derubify(tree)).smooth()
    return (s.replace(u"\u3000", " ") for s in tree.stripped_strings)


def count_tokens(lines) -> dict:
    frequency_dict = defaultdict(int)
    for line in lines:
        for token in (t.dictionary_form() for t in Tokenizer.tokenize(line, tokenizer.Tokenizer.SplitMode.B)):
            if CJK_PATTERN.match(token):
                frequency_dict[token] += 1
    return frequency_dict


def term_meta_bank(frequency_dict):
    """Convert frequency dict to term_meta_bank structure"""
    total_number_of_morphemes = len(frequency_dict.keys())
    result = []
    for index, morpheme in enumerate(sorted(frequency_dict, key=frequency_dict.get, reverse=True)):
        result.append([morpheme, "freq", f"{index + 1}/{total_number_of_morphemes}"])
    return result


def save_freqency_dict(title, term_meta_bank):
    output_path = f"{title}.zip"
    index_dict = {"title": title, "format": 3, "revision": "frequency1"}

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("index.json", json.dumps(index_dict, ensure_ascii=False))
        zip_file.writestr("term_meta_bank_1.json", json.dumps(term_meta_bank, ensure_ascii=False))


def book_to_freq(book_path, title=None):
    book = epub.read_epub(book_path)
    if not (book.title or title):
        raise ("Title required")

    save_freqency_dict(title if title is not None else book.title,
                       term_meta_bank(count_tokens(book_strings(book))))


def books_to_freq(book_paths, title=None):
    books = [epub.read_epub(book_path) for book_path in book_paths]
    if title is None:
        title = f"{books[0].title} freq"
    if title.endswith(".zip"):
        title = title[:-4]  # Strip .zip because zipfile adds it automatically
    save_freqency_dict(title, term_meta_bank(count_tokens(books_strings(books))))


def main():
    parser = argparse.ArgumentParser("yomifreq", description="Generate a Yomichan frequency list from one or more .epub files")
    parser.add_argument("--title", "-t", help="Title for output frequency dictionary")
    parser.add_argument("epubs", nargs="+", help="One or more epub files")
    args = parser.parse_args()
    books_to_freq(args.epubs, args.title)


if __name__ == '__main__':
    main()
