#!/usr/bin/env python3
import argparse  # -documentation: https://docs.python.org/3/howto/argparse.html
import collections
import configparser
import dataclasses
import enum
import os
import logging
import re
import sys
from collections import ChainMap
from string import Template
# -documentation: https://docs.python.org/3/library/string.html#template-strings
import distutils.dir_util
import distutils.file_util
import webbrowser
import datetime

INDEX_FILE: str = "index.html"
RSS_FILE: str = "rss.xml"
DATE_ONLY_IN_FORMAT: str = "%Y-%m-%d"
TAGS: str = "tags"
GENERAL_SECTION = "general"
SETTINGS = "settings.ini"


class PageTypeEnum(enum.Enum):
    standard = enum.auto()
    blog_post = enum.auto()
    blog_tag = enum.auto()


@dataclasses.dataclass(frozen=True)
class InitialValues:
    content_dir_path: str
    theme_dir_path: str
    output_dir_path: str
    content_base_url: str
    website_base_url: str


def get_html_from_file(i_path: str) -> str:
    ret_html: str = ""
    with open(i_path) as f:
        file_contents: str = f.read()
    if i_path.lower().endswith(".md"):
        # import commonmark  # -Unknown license
        # ret_html = commonmark.commonmark(file_contents)
        import mistletoe  # -Expat (MIT) license
        ret_html = mistletoe.markdown(file_contents)
    elif i_path.lower().endswith(".html"):
        ret_html = file_contents
    return ret_html


def get_datetime(i_content_file_path: str) -> datetime.datetime:
    file_name = os.path.basename(i_content_file_path)
    file_name_parts: list = file_name.split("_")
    if len(file_name_parts) >= 2:
        date_text: str = file_name_parts[0]
        try:
            dt = datetime.datetime.strptime(date_text, DATE_ONLY_IN_FORMAT)
            return dt
        except ValueError:
            pass
    unix_timestamp = int(os.path.getmtime(i_content_file_path))
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    return dt


def get_datetime_text(i_content_file_path: str) -> str:
    dt = get_datetime(i_content_file_path)
    ret_dt_text = dt.strftime("%d %B %Y")  # https://strftime.org/
    return ret_dt_text


def is_page(i_fd_name: str) -> bool:
    if i_fd_name.lower().endswith((".html", ".md")):
        return True
    return False


def is_resource_dir(i_fd_path: str) -> bool:
    if os.path.isdir(i_fd_path):
        base_name_str = os.path.basename(i_fd_path)
        if base_name_str.startswith("_"):
            return True
    return False


def create_html_from_template(i_theme_dir_path: str, i_nav: dict,
        i_content_fd_path: str, i_public_fd_path: str, i_html_content: str,
        i_page_type: PageTypeEnum) -> str:
    template_file_path: str = os.path.join(i_theme_dir_path, "template.html")
    public_fd_path_list = i_public_fd_path.split("/")
    if i_page_type == PageTypeEnum.standard:
        relative_link: str = ""
        active_nav_file: str = public_fd_path_list[-1]
    elif i_page_type == PageTypeEnum.blog_post:
        relative_link: str = "../"
        active_nav_file: str = public_fd_path_list[-2]
    elif i_page_type == PageTypeEnum.blog_tag:
        relative_link: str = "../../"
        active_nav_file: str = public_fd_path_list[-3]
    else:
        raise Exception("Case not covered")
    with open(template_file_path, "r") as template_file:
        template = Template(template_file.read())
        nav_total_str = ""
        for _fd_public_name, _nav_title_str in i_nav.items():
            nav_line_str = f'<a class="nav-item" href="{relative_link}{_fd_public_name}">{_nav_title_str}</a>'
            if remove_suffix(_fd_public_name) == remove_suffix(active_nav_file):  # -active page for blog post
                nav_line_str = f'<a id="active-nav-item" class="nav-item" href="{relative_link}{_fd_public_name}">{_nav_title_str}</a>'
                # -adding href here so that the user can navigate back to the blog overview page
            nav_total_str += nav_line_str
        website_title: str = get_title_text(os.path.basename(i_content_fd_path))
        ret_result: str = template.substitute(
            website_title=website_title,
            edit_url=i_content_fd_path,
            content=i_html_content,
            navigation=nav_total_str,
            internal_navigation=""
        )
        return ret_result


def remove_suffix(i_fd_name: str) -> str:
    file_name_wo_suffix: str = i_fd_name
    if "." in i_fd_name:
        file_name_wo_suffix = i_fd_name.rpartition(".")[0]
    return file_name_wo_suffix


def get_text_intro(post_fd_path: str) -> str:
    ret_snippet = get_html_from_file(post_fd_path)
    ret_snippet = re.sub(r"<[^>]+>", "", ret_snippet)
    ret_snippet: str = ret_snippet[:100]
    return ret_snippet


def copy_theme_files(i_theme_dir_path: str, i_dest_path: str) -> None:
    style_file_path: str = os.path.join(i_theme_dir_path, "style.css")
    favicon_file_path: str = os.path.join(i_theme_dir_path, "favicon.png")
    distutils.file_util.copy_file(style_file_path, i_dest_path)
    if os.path.isfile(favicon_file_path):
        distutils.file_util.copy_file(favicon_file_path, i_dest_path)


def get_title_text(i_fd_name: str) -> str:
    ret_title_str = remove_suffix(i_fd_name)
    ret_title_str = ret_title_str.split("[", maxsplit=1)[0]  # removing tags
    parts_list = ret_title_str.split("_")
    if len(parts_list) >= 2:
        potential_date_text = parts_list[0]
        try:
            datetime.datetime.strptime(potential_date_text, DATE_ONLY_IN_FORMAT)
            ret_title_str = "_".join(parts_list[1:])
        except ValueError:
            pass
    ret_title_str = ret_title_str.replace("_", " ").title()
    return ret_title_str


def get_page_title_html(i_fd_name: str, i_parent_name: str = "") -> str:
    title_text: str = get_title_text(i_fd_name)
    ret_string = "<h2>"
    if i_parent_name:
        ret_string += f'<span class="context">{i_parent_name}: </span>'
    ret_string += f"{title_text}</h2>"
    return ret_string


def get_public_file_name(i_fd_name: str) -> str:
    file_name_wo_suffix_str = remove_suffix(i_fd_name)
    ret_public_file_name_str = file_name_wo_suffix_str + ".html"
    return ret_public_file_name_str


# TODO: Using the same structure as for generate_html. How?
def get_nav_dict(i_content_base_dir_path: str) -> dict:
    ret_nav = collections.OrderedDict()
    top_content_fd_list = os.listdir(i_content_base_dir_path)
    for fd_name_str in top_content_fd_list:
        fd_content_path_str = os.path.join(i_content_base_dir_path, fd_name_str)
        public_file_name_str = get_public_file_name(fd_name_str)
        nav_title_str = get_title_text(fd_name_str)
        if is_page(fd_name_str):
            if fd_name_str.lower() == "readme.md":
                public_file_name_str = INDEX_FILE
            if public_file_name_str.lower() == INDEX_FILE:
                nav_title_str = "Home"
            ret_nav[public_file_name_str] = nav_title_str
        elif is_resource_dir(fd_content_path_str):
            pass
        elif os.path.isdir(fd_content_path_str):
            ret_nav[public_file_name_str] = nav_title_str
            # ret_nav.move_to_end(public_file_name_str)
    ret_nav.move_to_end(INDEX_FILE, last=False)
    return dict(ret_nav)


def get_tags(i_sub_fd_name: str) -> list:
    regexp: str = r"\[([^]]+)"
    ret_tags = re.findall(regexp, i_sub_fd_name)
    return ret_tags


def get_input_path(i_base_dir: str, i_argument_dir) -> str:
    """Takes a base dir, and relative or absolute path. Returns an absolute path."""
    if not i_argument_dir:
        raise Exception("Second argument cannot be empty")
    if os.path.isdir(i_argument_dir):  # -relative to the pwd of the user
        absolute_path = os.path.abspath(i_argument_dir)
    else:  # -relative to the base dir
        absolute_path = os.path.join(i_base_dir, i_argument_dir)
    return absolute_path


def get_output_path(i_argument_dir: str, i_force_remove_output: bool) -> str:
    """Takes a relative or absolute path. Creates a dir (possibly after removing it).
    Returns an absolute path"""
    if os.path.isdir(i_argument_dir):
        remove_output_bool = False
        if not i_force_remove_output:
            user_input: str = input(f"The dir {i_argument_dir} is not empty. "
            "Are you sure you want to remove the contents in it? (y/n)")
            remove_output_bool = user_input == "y"
        if remove_output_bool or i_force_remove_output:
            distutils.dir_util.remove_tree(i_argument_dir)
        else:
            print("Exiting")
            sys.exit(0)
    absolute_path = os.path.abspath(i_argument_dir)
    os.mkdir(absolute_path)
    return absolute_path


def generate_post_html(i_init_vals: InitialValues, i_fd_path: str, i_nav: dict,
        i_post_content_file_path: str) -> str:
    post_name = os.path.basename(i_post_content_file_path)
    post_fd_path = os.path.join(
        i_init_vals.content_dir_path, os.path.basename(i_fd_path), post_name)
    # parent_title = get_public_file_name(i_fd_name)
    sub_html_content_str = get_page_title_html(post_name)
    sub_html_content_str += get_html_from_file(post_fd_path)
    result_str = create_html_from_template(i_init_vals.theme_dir_path, i_nav, post_fd_path,
        i_post_content_file_path, sub_html_content_str, PageTypeEnum.blog_post)
    return result_str


def generate_post_snippet(i_public_dir_name, i_post_fd_path, i_tags_for_page: list,
        i_post_descr) -> str:
    post_fd_name: str = os.path.basename(i_post_fd_path)
    post_date_text: str = get_datetime_text(i_post_fd_path)
    post_public_file_name: str = get_public_file_name(post_fd_name)
    post_title: str = get_title_text(post_fd_name)
    rel_post_public_path_fd = os.path.join(i_public_dir_name, post_public_file_name)
    # -path is relative to the output directory
    tags_html_list = []
    for tag_name in i_tags_for_page:
        tag_file_name = tag_name + ".html"
        rel_tag_file_path: str = os.path.join(i_public_dir_name, TAGS, tag_file_name)
        tags_html_list.append(f'<span><a href="{rel_tag_file_path}">#{tag_name}</a></span>')
    tags_html = ", ".join(tags_html_list)
    ret_snippet_html: str = f"""<div><h3><a href="{rel_post_public_path_fd}">{post_title}</a></h3>
    {tags_html}<span> --- {post_date_text}</span>
    <p>{i_post_descr}</p>
    </div>"""
    return ret_snippet_html


def generate_blog_html(i_init_vals: InitialValues, i_nav: dict, i_content_fd_path: str) -> dict:
    result_output_dict = {}
    public_dir_path = os.path.join(i_init_vals.output_dir_path, os.path.basename(i_content_fd_path))
    os.mkdir(public_dir_path)  # -we need to create the new dir ourselves
    copy_theme_files(i_init_vals.theme_dir_path, public_dir_path)
    blog_name: str = os.path.basename(i_content_fd_path)
    blog_content_fd_path_list = []
    for fd_name in os.listdir(i_content_fd_path):
        fd_path = os.path.join(i_content_fd_path, fd_name)
        blog_content_fd_path_list.append(fd_path)
    blog_page_html = get_page_title_html(os.path.basename(i_content_fd_path))
    tag_dict = {}

    appl_base_dir_path: str = os.path.dirname(os.path.abspath(__file__))
    rss_item_template_file_path = os.path.join(appl_base_dir_path, "rss_item.xml")
    with open(rss_item_template_file_path, "r") as template_file:
        rss_item_template = Template(template_file.read())
    rss_items_xml: str = ""

    feed_template_file_path = os.path.join(appl_base_dir_path, "rss_feed.xml")
    with open(feed_template_file_path, "r") as template_file:
        rss_feed_template = Template(template_file.read())

    for post_content_file_path in sorted(blog_content_fd_path_list, key=lambda x: get_datetime(x)):
        post_name = os.path.basename(post_content_file_path)
        if not is_page(post_name):
            continue

        # A. Create post html
        post_public_file_name: str = get_public_file_name(post_name)
        post_public_file_path: str = os.path.join(i_init_vals.output_dir_path, blog_name,
            post_public_file_name)
        post_html = generate_post_html(i_init_vals, i_content_fd_path, i_nav,
            post_content_file_path)
        result_output_dict[post_public_file_path] = post_html

        # B. Building tags lists
        tags_for_page: list = get_tags(post_name)
        for tag in tags_for_page:
            post_list = []
            if tag in tag_dict:
                post_list = tag_dict.get(tag)
            post_list.append(post_public_file_name)
            tag_dict[tag] = post_list

        # C. Building list of blog entries on blog post_public_fn
        post_descr: str = get_text_intro(post_content_file_path)
        blog_page_html += generate_post_snippet(blog_name, post_content_file_path, tags_for_page,
            post_descr)

        # D. Creating RSS items for the post
        blog_post_public_file_name = get_public_file_name(post_name)
        if i_init_vals.website_base_url.endswith("/"):
            website_base_url = i_init_vals.website_base_url
        else:
            website_base_url = i_init_vals.website_base_url + "/"
        blog_post_public_file_url = website_base_url + os.path.join(blog_name,
            blog_post_public_file_name)
        blog_post_title = get_title_text(blog_post_public_file_name)
        item_string = rss_item_template.substitute(
            title=blog_post_title,
            link=blog_post_public_file_url,
            description=post_descr
        )
        rss_items_xml += item_string

    tags_dir_path: str = os.path.join(i_init_vals.output_dir_path, blog_name, TAGS)
    os.mkdir(tags_dir_path)
    copy_theme_files(i_init_vals.theme_dir_path, tags_dir_path)

    # Creating a page for each tag
    for tag_name, post_list in tag_dict.items():
        tag_file_name: str = tag_name + ".html"
        tag_file_path: str = os.path.join(tags_dir_path, tag_file_name)
        inner_tag_page_html = f"<p>{tag_name}</p><ul>"
        for post_public_fn in post_list:
            inner_tag_page_html += f'<li><a href="../{post_public_fn}">{post_public_fn}</a></li>'
        inner_tag_page_html += "</ul>"
        tag_page_html = create_html_from_template(i_init_vals.theme_dir_path, i_nav,
            i_content_fd_path, tag_file_path, inner_tag_page_html, PageTypeEnum.blog_tag)
        result_output_dict[tag_file_path] = tag_page_html

    # Creating an RSS feed..
    if i_init_vals.website_base_url:
        title: str = get_title_text(os.path.basename(i_init_vals.content_dir_path))
        rss_all_content_xml: str = rss_feed_template.substitute(
            title=title, link=i_init_vals.website_base_url,
            description="WEBSITE DESCR", items=rss_items_xml
        )
        rss_public_file_path_str = os.path.join(i_init_vals.output_dir_path, blog_name, RSS_FILE)
        result_output_dict[rss_public_file_path_str] = rss_all_content_xml
        # ..and linking to it on the blog page
        rel_rss_feed_file_path = os.path.join(blog_name, RSS_FILE)
        blog_page_html += f"<hr><a href={rel_rss_feed_file_path}>RSS feed</a>"

    public_file_name_str = get_public_file_name(os.path.basename(i_content_fd_path))
    public_file_path_str = os.path.join(i_init_vals.output_dir_path, public_file_name_str)
    post_html = create_html_from_template(i_init_vals.theme_dir_path,
        i_nav, i_content_fd_path, public_file_path_str, blog_page_html, PageTypeEnum.standard)
    result_output_dict[public_file_path_str] = post_html

    return result_output_dict


def generate_public_html(i_initial_values: InitialValues) -> dict:
    copy_theme_files(i_initial_values.theme_dir_path, i_initial_values.output_dir_path)
    nav_dict = get_nav_dict(i_initial_values.content_dir_path)
    fd_name_list = os.listdir(i_initial_values.content_dir_path)
    result_output_dict = {}
    for fd_name in fd_name_list:
        fd_path: str = os.path.join(i_initial_values.content_dir_path, fd_name)
        edit_url: str = os.path.join(i_initial_values.content_base_url, fd_name)
        public_file_name = get_public_file_name(fd_name)
        if fd_name.lower() == "readme.md":
            # and INDEX_FILE not in fd_name_list and "index.md" not in fd_name_list
            public_file_name = INDEX_FILE
        if is_resource_dir(fd_path):  # -this might be an _img directory
            public_dir_path_str = os.path.join(i_initial_values.output_dir_path, fd_name)
            os.mkdir(public_dir_path_str)  # -we need to create the new dir ourselves
            distutils.dir_util.copy_tree(fd_path, public_dir_path_str)
        elif os.path.isdir(fd_path):  # -blog
            blog_output_dict = generate_blog_html(i_initial_values, nav_dict, fd_path)
            result_output_dict.update(blog_output_dict)
        elif is_page(fd_name):
            html_from_file = get_html_from_file(fd_path)
            html_content_str = ""
            if (not html_from_file.strip().lower().startswith("<h")
                    and not fd_name.lower().startswith(INDEX_FILE)):
                html_content_str += get_page_title_html(fd_name)
            html_content_str += html_from_file
            public_file_path = os.path.join(i_initial_values.output_dir_path, public_file_name)
            result_str = create_html_from_template(i_initial_values.theme_dir_path, nav_dict,
                fd_path, public_file_path, html_content_str, PageTypeEnum.standard)
            result_output_dict[public_file_path] = result_str
        elif fd_name.startswith("."):  # -ex: .gitkeep
            pass
        elif os.path.isfile(fd_path):
            logging.debug(f"{fd_name} is not processed")
        else:
            logging.warning(f"{fd_name} is neither a file nor a directory")
    return result_output_dict


CONTENT_DIR = "content_dir"
THEME_DIR = "theme_dir"
OUTPUT_DIR = "output_dir"
FORCE_REMOVE_OUTPUT = "force_remove_output"
CONTENT_URL = "content_url"
WEBSITE_URL = "website_url"


def get_initial_values() -> InitialValues:
    """Get values from argparse and configparser, and create initial values based on this"""
    appl_base_dir_path: str = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"{appl_base_dir_path = }")
    appl_theme_dir_path: str = os.path.join(appl_base_dir_path, "themes")
    availalbe_themes: [str] = os.listdir(appl_theme_dir_path)

    def get_long_arg(i_cli_arg: str):
        ret_long_cli_arg: str = "--" + i_cli_arg.replace('_', '-')
        return ret_long_cli_arg

    argument_parser = argparse.ArgumentParser(
        prog="Website Generator", description="A minimalistic static website generator")
    # All dashes (-) are converted to underscores
    argument_parser.add_argument(get_long_arg(CONTENT_DIR), "-d",
        help="Base dir containing the website (input) content")
    argument_parser.add_argument(get_long_arg(THEME_DIR), "-t",
        help="Path to dir containing the theme, or the name of a built-in theme. "
        "These are the built-in themes: " + ", ".join(availalbe_themes))
    argument_parser.add_argument(get_long_arg(OUTPUT_DIR), "-o",
        help="Path to base dir which will recieve the output (html etc) which will make up the "
             "whole website")
    argument_parser.add_argument(get_long_arg(FORCE_REMOVE_OUTPUT), "-f",
        action=argparse.BooleanOptionalAction,
        help="(true/false) No prompt if and when overwriting the output dir.")
    argument_parser.add_argument(get_long_arg(CONTENT_URL), "-c",
        help="Base URL for editing content online. Only used when your content is hosted remotely")
    argument_parser.add_argument(get_long_arg(WEBSITE_URL), "-w",
        help="Base URL for the website. Needed for generating RSS feeds")
    # , default=""
    tmp_args: dict = vars(argument_parser.parse_args())
    cli_args = {}
    for k, v in tmp_args.items():
        if v is not None:
            cli_args[k] = v

    config_parser = configparser.ConfigParser()
    config_parser.read(SETTINGS)
    tmp_config = {}
    try:
        tmp_config = dict(config_parser[GENERAL_SECTION])
    except KeyError:
        pass
    file_config = {}
    for k, v in tmp_config.items():
        k: str
        k = k.replace('-', '_')
        if k == FORCE_REMOVE_OUTPUT:
            file_config[k] = False
            fro_config_file_key: str = FORCE_REMOVE_OUTPUT.replace('_', '-')
            file_config[k] = config_parser.getboolean(GENERAL_SECTION, fro_config_file_key)
            # -raises ValueError if unclear
        else:
            file_config[k] = v

    default_params = {
        CONTENT_DIR: "example-content",
        THEME_DIR: "side-nav",
        OUTPUT_DIR: "public",
        FORCE_REMOVE_OUTPUT: False,
        CONTENT_URL: "",
        WEBSITE_URL: "",
    }

    params_chainmap = ChainMap(cli_args, file_config, default_params)
    # -inspired by one of the answers here: https://stackoverflow.com/q/48538581/2525237

    content_dir_path = get_input_path(appl_base_dir_path, params_chainmap[CONTENT_DIR])
    logging.info(f"{content_dir_path = }")
    theme_dir_path = get_input_path(appl_theme_dir_path, params_chainmap[THEME_DIR])
    logging.info(f"{theme_dir_path = }")
    output_dir_path = get_output_path(
        params_chainmap[OUTPUT_DIR], params_chainmap[FORCE_REMOVE_OUTPUT])
    logging.info(f"{output_dir_path = }")
    content_base_url = params_chainmap[CONTENT_URL]
    logging.info(f"{content_base_url = }")
    website_base_url = params_chainmap[WEBSITE_URL]
    logging.info(f"{website_base_url = }")

    ret_initial_values = InitialValues(
        content_dir_path, theme_dir_path, output_dir_path, content_base_url, website_base_url)
    return ret_initial_values


def main():
    logging.basicConfig(level=logging.DEBUG)
    initial_values = get_initial_values()
    output_dict: dict = generate_public_html(initial_values)
    for public_file_path, result_data_str in output_dict.items():
        with open(public_file_path, "w+") as output_file:
            output_file.write(result_data_str)
    webbrowser.open(os.path.join(initial_values.output_dir_path, INDEX_FILE))  # -preview


if __name__ == "__main__":
    main()
