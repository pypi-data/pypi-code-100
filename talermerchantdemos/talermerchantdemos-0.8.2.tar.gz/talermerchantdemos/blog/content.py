##
# This file is part of GNU TALER.
# Copyright (C) 2014-2020 Taler Systems SA
#
# TALER is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation; either version 2.1, or (at your option) any later version.
#
# TALER is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with
# GNU TALER; see the file COPYING.  If not, see <http://www.gnu.org/licenses/>
#
# @author Florian Dold
# @brief Define content and associated metadata that is served on the blog.

from collections import OrderedDict, namedtuple
import logging
import os
import re
from bs4 import BeautifulSoup
from pkg_resources import resource_stream, resource_filename
from os import listdir
from os.path import isfile, join
from urllib.parse import quote


LOGGER = logging.getLogger(__name__)
NOISY_LOGGER = logging.getLogger("chardet.charsetprober")
NOISY_LOGGER.setLevel(logging.INFO)
Article = namedtuple("Article", "slug title teaser main_file extra_files lang")

##
# @var if a article is added to this list, then it will
#      be made available in the blog.
#      ARTICLES is a dict mapping a languguage ('en') to an OrderedDict() of
#      articles available in that language.
ARTICLES = {}


##
# Add article to the list of the available articles.
#
# @param slug article's title with all the spaces converted to underscores.
# @param title article's title.
# @param teaser a short description of the main article's content.
# @param main_file path to the article's HTML file.
# @param extra_file collection of extra files associated with the
#        article, like images and sounds.
# @param lang language of the arcile
def add_article(slug, title, teaser, main_file, extra_files, lang="en"):
    if not (lang in ARTICLES):
        ARTICLES[lang] = OrderedDict()
    ARTICLES[lang][slug] = Article(slug, title, teaser, main_file, extra_files, lang)


##
# Build the file path of a image.
#
# @param image the image filename.
# @return the path to the image file.
def get_image_file(image):
    filex = resource_filename("talermerchantdemos", os.path.join("blog/data/", image))
    return os.path.abspath(filex)


##
# Build the file path of a article.
#
# @param article the article filename.
# @return the path to the article HTML file.
def get_article_file(article):
    filex = resource_filename(
        "talermerchantdemos", article.main_file,
    )
    return os.path.abspath(filex)


##
# Extract information from HTML file, and use these informations
# to make the article available in the blog.
#
# @param resource_name path to the (HTML) article.
# @param teaser_paragraph position of the teaser paragraph in the
#        article's list of all the P tags.  Defaults to zero, as normally
#        this information is found under the very first P tag.
# @param title article's title; normally, this bit is extracted from the
#        HTML itself, so give it here if a explicit title needs to be
#        specified.
def add_from_html(resource_name, lang):
    res = resource_stream("talermerchantdemos", resource_name)
    soup = BeautifulSoup(res, "html.parser")
    res.close()
    title_el = soup.find("h2")
    if title_el is None:
        LOGGER.warning("Cannot extract title from '%s'", resource_name)
        title = resource_name
    else:
        title = title_el.get_text().strip()
    slug = quote(title.replace(" ", "_"), safe="")

    teaser = soup.find("p", attrs={"id": ["teaser"]})
    if teaser is None:
        paragraphs = soup.find_all("p")
        if len(paragraphs) > 0:
            teaser = paragraphs[0].get_text()
            if (len(paragraphs) > 1) and (len(teaser) < 100):
                teaser2 = paragraphs[1].get_text()
                if len(teaser2) > len(teaser):
                    teaser = teaser2
        else:
            LOGGER.warning("Cannot extract teaser from '%s'", resource_name)
            teaser = ""
    else:
        teaser = teaser.get_text()
    re_proc = re.compile("^/[^/][^/]/essay/[^/]+/data/[^/]+$")
    imgs = soup.find_all("img")
    extra_files = []
    for img in imgs:
        # We require that any image whose access is regulated is src'd
        # as "<slug>/data/img.png". We also need to check if the <slug>
        # component actually matches the article's slug
        if re_proc.match(img["src"]):
            if img["src"].split(os.sep)[2] == slug:
                LOGGER.info(
                    "extra file for %s is %s" % (slug, os.path.basename(img["src"]))
                )
                extra_files.append(os.path.basename(img["src"]))
            else:
                LOGGER.warning(
                    "Image src and slug don't match: '%s' != '%s'"
                    % (img["src"].split(os.sep)[2], slug)
                )
    add_article(slug, title, teaser, resource_name, extra_files, lang)


for l in listdir(resource_filename("talermerchantdemos", "blog/articles/")):
    # Filter by active languages, otherwise this takes quite a while to load...
    if l in {"en", "ar", "zh", "fr", "hi", "it", "ja", "ko", "pt", "pt_BR", "ru", "tr", "de", "sv", "es"}:
        LOGGER.info("importing %s" % l)
        for a in listdir(resource_filename("talermerchantdemos", "blog/articles/" + l)):
            add_from_html("blog/articles/" + l + "/" + a, l)
