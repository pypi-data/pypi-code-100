#!/usr/bin/python3
"""
    ptinsearcher

    Copyright (c) 2020 HACKER Consulting s.r.o.

    ptinsearcher is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ptinsearcher is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ptinsearcher.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0.4"

import argparse
import html
import os
import re
import stat
import sys
import tempfile
import urllib

from ptlibs import ptmisclib, ptjsonlib
from bs4 import BeautifulSoup

import exiftool
import tldextract
import requests


class ptinsearcher:
    def __init__(self, args):
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.json_no = self.ptjsonlib.add_json("ptinsearcher")
        self.ptjsonlib.add_data(self.json_no, {"urls": []})

        self.headers = ptmisclib.get_request_headers(args)
        self.proxies = {"http": args.proxy, "https": args.proxy}
        self.timeout = 15

        self.post_data = args.post_data
        self.method = "GET" if not args.post_data else "POST"
        self.redirects = args.redirects
        self.domain = self.get_domain(args.domain)

        self.url_list = self.get_url_list(args)
        self.extract_types = self.get_extract_types(args.extract)

        if args.grouping and args.grouping_complete:
            ptmisclib.end_error("Cannot use both -g and -gc parameters together", self.json_no, self.ptjsonlib, self.use_json)
        self.grouping = args.grouping
        self.grouping_complete = args.grouping_complete

        self.group_parameters = args.group_parameters
        self.without_parameters = args.without_parameters

        self.fh = None
        self.output_file  = args.output
        self.output_parts = args.output_parts

        if args.output and not os.path.exists(os.path.join(os.path.expanduser('~'), SCRIPTNAME)):
            os.makedirs(os.path.join(os.path.expanduser('~'), SCRIPTNAME))
        if args.output_parts and not args.output:
            ptmisclib.end_error("Missing -o/--output parameter", self.json_no, self.ptjsonlib, self.use_json)
        if args.output and not args.output_parts:
            self.fh = open(os.path.join(os.path.expanduser('~'), SCRIPTNAME, self.output_file), "w")
                
    def run(self):
        self._iterate_websites()
        if self.grouping or self.grouping_complete and not self.use_json:
            self.print_dictionary(self.ptjsonlib.json_list[0]["data"]["urls"])
        if self.fh:
            self.fh.close()
        ptmisclib.ptprint(ptmisclib.out_if(self.ptjsonlib.get_all_json(), "", self.use_json), end="")

    def _iterate_websites(self):
        for url in self.url_list:
            self.url = url
            self.data = {"url": "null", "status": "null", "vulnerable:": "null", "content-type": "null", "data": []}
            ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Testing: {url}", self.use_json))

            if os.path.exists(self.url):
                if not os.path.isabs(self.url):
                    self.url = os.path.abspath(self.url)
                self.scrape_website(self.url, is_file=True)

            else:
                try:
                    response = requests.request(self.method, url, allow_redirects=self.redirects, timeout=self.timeout, headers=self.headers, proxies=self.proxies, verify=False, data=self.post_data)
                    response.encoding = response.apparent_encoding
                except Exception as e:
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"Server not responding", "ERROR", self.use_json))
                    self.data.update({"status": "error", "message": str(e)})
                    continue

                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Response: {response.url} [{response.status_code}]", "INFO", self.use_json), end=" ")
                if response.headers.get("location"):
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"-> {ptmisclib.get_colored_text(response.headers['location'], 'ERROR')}", "", self.use_json))
                ptmisclib.ptprint(ptmisclib.out_ifnot(" ", "", self.use_json))
                if str(response.status_code).startswith("3") and not self.redirects:
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"Redirects disabled, not following ", "ERROR", self.use_json))
                    self.data.update({"status": "error", "message": f"response status code {response.status_code}, but redirects are disabled, skipping this test"})
                    self.data.update({"url": response.url})
                    self.ptjsonlib.add_data(self.json_no, self.data)
                    continue
                self.process_response(response)

    def process_response(self, response):
        TEXT_CONTENT = ["text/html", "text/plain", "text/css", "text/cvs", "text/javascript", "application/json", "application/xml"]
        XML_CONTENT = ["application/xml", "text/xml"]
        content_type = response.headers.get("content-type").split(";")[0]
        ptmisclib.ptprint(ptmisclib.out_ifnot(f"Content-Type: {content_type}", "INFO", self.use_json))

        self.data.update({"url": response.url, "status": "ok", "content-type": content_type})
        if content_type == "text/plain" and response.url.endswith("robots.txt"):
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"File-type: robots.txt", "INFO", self.use_json))
            self.parse_robots_txt(response)
        elif content_type in TEXT_CONTENT:
            self.scrape_website(response)
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Unknown content-type: {content_type}, trying to extract metadata...", "INFO", self.use_json))
            self.extract_types = self.get_extract_types("M")
            self.scrape_metadata(response.content)

    def parse_robots_txt(self, response):
        allow = list({pattern.lstrip() for pattern in re.findall(r"^Allow: ([\S ]*)", response.text, re.MULTILINE)})
        disallow = list({pattern.lstrip() for pattern in re.findall(r"^Disallow: ([\S ]*)", response.text, re.MULTILINE)})
        sitemaps = re.findall(r"[Ss]itemap: ([\S ]*)", response.text, re.MULTILINE)
        robots_data = {"disallow": disallow, "allow": allow, "sitemaps": sitemaps}
        self.ptjsonlib.add_data(self.json_no, robots_data)
        if not self.use_json:
            for key, value in robots_data.items():
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"\n{key.capitalize()}:\n{'-'*(len(key)+1)}", "", self.use_json))
                ptmisclib.ptprint(ptmisclib.out_ifnot('\n'.join(value), "", self.use_json))

    def get_metadata(self, response_content):
        executable = os.path.join(os.path.dirname(os.path.realpath(__file__)), "utils", "ExifTool", "exiftool")
        is_executable = os.access(executable, os.X_OK)
        if not is_executable:
            try:
                os.chmod(executable, os.stat(executable).st_mode | stat.S_IEXEC)
            except:
                ptmisclib.end_error(f"Cannot execute nor set execution privileges for exiftool, try running 'sudo chmod +x {executable}'", self.json_no, self.ptjsonlib, self.use_json)
        with tempfile.NamedTemporaryFile(mode="w+b", suffix="") as tmpfile:
            tmpfile.write(response_content)
            tmpfile.flush()
            with exiftool.ExifTool(executable_=executable) as et:
                metadata = et.get_metadata(tmpfile.name)
                blacklist = ["SourceFile", "ExifTool:ExifToolVersion", "File:FileName", "File:Directory"]
                for i in blacklist:
                    if metadata.get(i):
                        metadata.pop(i)
                return metadata
 
    def scrape_metadata(self, response_content):
        metadata = self.get_metadata(response_content)
        self.data["data"].append({"metadata": metadata})
        self.ptjsonlib.json_list[0]["data"]["urls"].append(self.data)
        if not self.use_json and not (self.grouping or self.grouping_complete):
            self.print_dictionary([self.ptjsonlib.json_list[0]["data"]["urls"][-1]])

    def scrape_website(self, response, is_file=False):
        """Extracts information from HTML page"""
        re_comment = r'<!--[\s\w\W]*?-->'
        re_email = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,3}'
        re_ip = r'(?<![\.\+\-])\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
        re_phone = r"(?<![\w\/=\:-])(\(?\+\d{3}\)?[ -]?)?(\d{3}[ -]?)(\d{2,3}[ -]?)(\d{3}|\d{2} \d{2})(?![\w\"\'\/\\.])"
        re_abs_url = r'(https?|ftps?)(://[\w\.]*\.[a-zA-Z]{2,3}[?&/#]*[^"\'><\s]*)'
        re_relative_url = r'(href=|src=)[\'"](.+?)[\'"]'
        re_possible_links = r"(((http|ftp|https|irc)://)|(www\.))([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?" # File situation only

        comments                             =      None
        phone_numbers                        =      None
        emails                               =      None
        ip_addresses                         =      None
        abs_urls                             =      None
        forms                                =      None
        subdomains                           =      None
        internal_urls                        =      None
        external_urls                        =      None
        metadata                             =      None
        parsed_internal_urls_with_parameters =      None
        found_infile_links                   =      None

        if not is_file:
            soup = self.get_soup(response)
            page_content = urllib.parse.unquote(urllib.parse.unquote(html.unescape(soup.prettify())))
        else:
            with open(response, "rb") as f:
                page_content = f.read()
                if self.extract_types["metadata"]:
                    metadata = self.get_metadata(page_content)
                page_content = page_content.decode("utf-8")

        if self.extract_types["html_comments"]:
            comments =   self._find(page_content, re_comment)
        if self.extract_types["phone_numbers"]:
            phone_numbers = sorted(self._find(page_content, re_phone))
            phone_numbers = self.filter_phones(phone_numbers)
        if self.extract_types["emails"]:
            emails = self._find(page_content, re_email)
        if self.extract_types["ip_addresses"]:
            ip_addresses = (self._find(page_content, re_ip))
        if is_file:
            if self.extract_types["internal_urls"] or self.extract_types["external_urls"] or self.extract_types["internal_urls_with_parameters"] or self.extract_types["subdomains"]:
                found_infile_links = self._find(page_content, re_possible_links)
                found_infile_links = sorted(list(set(found_infile_links)), key=str.lower)
        if not is_file:
            if self.extract_types["internal_urls"] or self.extract_types["external_urls"] or self.extract_types["internal_urls_with_parameters"] or self.extract_types["subdomains"]:
                abs_urls = self._find(page_content, re_abs_url)
            if self.extract_types["internal_urls"] or self.extract_types["internal_urls_with_parameters"]:
                internal_urls = self.find_urls(page_content, re_relative_url, response.url, "internal", abs_urls)
            if self.extract_types["internal_urls_with_parameters"]:
                parsed_internal_urls_with_parameters = self._sort(self.find_internal_parameters(internal_urls))
            if self.extract_types["external_urls"]:
                external_urls = self.find_urls(page_content, re_relative_url, response.url, "external", abs_urls)
            if self.extract_types["subdomains"]:
                subdomains = self.find_urls(page_content, re_relative_url, response.url, "subdomain", abs_urls)
            if self.extract_types["forms"]:
                forms = self.get_forms(soup)
            if self.extract_types["metadata"]:
                metadata = self.get_metadata(response.content)

        result_data = {
            "html_comments": comments,
            "emails": emails,
            "phone_numbers": phone_numbers,
            "ip_addresses": ip_addresses,
            "internal_urls": internal_urls,
            "internal_urls_with_parameters": parsed_internal_urls_with_parameters,
            "external_urls": external_urls,
            "subdomains": subdomains,
            "forms": forms,
            "metadata": metadata,
            "found_infile_links": found_infile_links}

        self.data["data"].append(result_data)
        self.ptjsonlib.json_list[0]["data"]["urls"].append(self.data)
        if not self.use_json and not (self.grouping or self.grouping_complete):
            self.print_dictionary([self.ptjsonlib.json_list[0]["data"]["urls"][-1]], is_file)

    def find_urls(self, page_content, re_pattern, url, type_urls, result_old=[]):
        rslt = []
        domain = self.url2domain(url)
        all_urls = list({result[1] for result in re.findall(re_pattern, page_content)}) + result_old
        for found_url in all_urls:
            if found_url.startswith("mailto:") or found_url.startswith("javascript:"): 
                continue
            if found_url.startswith("//"):
                o = urllib.parse.urlparse(self.url)
                all_urls.append(o.scheme + ":" + found_url)
                continue
            abs_url = self.rel2abs(found_url, domain)
            o = urllib.parse.urlparse(abs_url)
            if self.without_parameters:
                abs_url = urllib.parse.urlunsplit((o[0], o[1], o[2], "", ""))
            if type_urls == "external" and (self.url2domain(abs_url, False, False) != self.url2domain(url, False, False)):
                rslt.append(abs_url)
            if (type_urls == "subdomain") and (self.url2domain(abs_url, False, False) == self.url2domain(url, False, False)):
                rslt.append(o.netloc)
                rslt.append(o.netloc)
            if type_urls == "internal" and (self.url2domain(abs_url, True, False) == self.url2domain(url, True, False)):
                rslt.append(abs_url)
        return sorted(list(set(rslt)), key=str.lower)

    def filter_phones(self, phone_list):
        result = []
        for n in phone_list:
            tmp = ''.join(n.split())
            tmp = tmp.replace("-", "")
            if tmp.startswith("+"):
                req_len = len(tmp[1:])
            else:
                req_len = len(tmp)
            if req_len in [9, 12]:
                if n not in result:
                    result.append(n)
        return result

    def _sort(self, url_list):
        return sorted(url_list, key=lambda k: k['url']) 

    def url2domain(self, url, with_subdomains=True, with_protocol=True):
        """Returns domain from supplied url"""
        tsd, td, tsu = tldextract.extract(url)
        if tsd: 
            tsd = tsd + "."
        if with_protocol:
            protocol = url.split("//")[0]
        else:
            protocol = "" 
        if with_subdomains:
            if not tsu:
                return protocol + "//" + tsd + td
            return protocol + "//" + tsd + td + "." + tsu
        else:
            if not tsu:
                return protocol + "//" + td + "." + tsu
            return protocol + "//" + td + "." + tsu

    def print_dictionary(self, dict_list, is_file=False):
        if dict_list:
            order_pattern = ["html_comments", "emails", "phone_numbers", "ip_addresses", "internal_urls", "internal_urls_with_parameters", "external_urls", "subdomains", "metadata", "forms"]
            selection = list(k for k, v in self.extract_types.items() if v == True and k != "all")
            selection = sorted(selection, key=order_pattern.index)
            if is_file:
                for i in ["internal_urls", "internal_urls_with_parameters", "external_urls", "subdomains", "forms"]:
                    if i in selection:
                        selection.remove(i)
                selection.append("found_infile_links")
            for i in selection:
                if self.grouping_complete:
                    grouping_result = set()
                if self.output_parts:
                    self.fh = open(os.path.join(os.path.expanduser('~'), SCRIPTNAME, f"{self.output_file}({i[0].upper()}).txt"), "w")
                ptmisclib.ptprint(ptmisclib.out_ifnot(f'\n{ptmisclib.get_colored_text(i.upper().replace("_", " "), color="TITLE")}\n{"=" * len(i)}', condition=self.use_json), filehandle=self.fh)
                sep = "\n"
                for idx, d in enumerate(dict_list):
                    if not d["data"][0][i]:
                        ptmisclib.ptprint(ptmisclib.out_ifnot(f"", "", self.use_json), end=self.check_if_next(dict_list, idx, i), filehandle=self.fh)
                        continue
                    if self.grouping:
                        ptmisclib.ptprint(ptmisclib.out_ifnot(ptmisclib.get_colored_text(f"{d['url']}", 'INFO'), None, self.use_json), filehandle=self.fh) # prints url of tested site
                    if i == "html_comments":
                        sep += "\n"
                    if i == "internal_urls_with_parameters":
                        self.print_parsed_urls(d["data"][0]["internal_urls_with_parameters"], dict_list, idx)
                        continue
                    if i == "forms":
                        self.print_forms(d["data"][0]["forms"])
                        continue
                    if i == "metadata":
                        self.print_metadata(d["data"][0]["metadata"], dict_list, idx)
                        continue
                    if self.grouping_complete:
                        grouping_result.add(sep.join(d['data'][0][i]))
                    else:
                        ptmisclib.ptprint(ptmisclib.out_ifnot(sep.join(d['data'][0][i]), condition=self.use_json), end=self.check_if_next(dict_list, idx, i)+"\n", filehandle=self.fh)

                if self.grouping_complete:
                    ptmisclib.ptprint(ptmisclib.out_ifnot(sep.join(grouping_result), condition=self.use_json), end=self.check_if_next(dict_list, idx, i)+"\n", filehandle=self.fh)
            print("")
            if self.fh:
                self.fh.close()

    def check_if_next(self, dict_list, idx, i):
        try:
            endl = "\n" if dict_list[idx+1]["data"][0][i] and not self.grouping_complete else ""
        except IndexError:
            endl = ""
        return endl

    def print_parsed_urls(self, result_list, dict_list, idx):
        for d in result_list:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"URL: {d['url']}", "", self.use_json), filehandle=self.fh)
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Parameters:", "", self.use_json), filehandle=self.fh)
            for l in d['parameters']:
                for i in l:
                    ptmisclib.ptprint(ptmisclib.out_ifnot('          ' + i), "\n", self.use_json, filehandle=self.fh)
                if d is not result_list[-1]:
                    ptmisclib.ptprint(ptmisclib.out_ifnot(' '), "\n", self.use_json, filehandle=self.fh)
            ptmisclib.ptprint(ptmisclib.out_ifnot(self.check_if_next(dict_list, idx, 'metadata'), "", self.use_json), end="", filehandle=self.fh)
            
    def print_forms(self, form_list):
        for form in form_list:
            for key, value in form.items():
                space = 0 if key == "form_name" else 9
                if key == "inputs" or key == "selects":
                    if not form[key]:
                        continue
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"\n{' '*space}{key.title()}:", "", self.use_json), filehandle=self.fh)
                    space += len(key)
                    for dictionary in form[key]:
                        for key, value in dictionary.items():
                            if key == "options":
                                ptmisclib.ptprint(ptmisclib.out_ifnot(f"{' '*space}{key.title()}:", "", self.use_json), filehandle=self.fh)
                                space += len(key)
                                for option in dictionary[key]:
                                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"{' '*space}{option}", "", self.use_json), filehandle=self.fh)
                            else:
                                ptmisclib.ptprint(ptmisclib.out_ifnot(f"{' '*space}{key.title()}: {value}", "", self.use_json), filehandle=self.fh)
                        #ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json), filehandle=self.fh)       
                else:
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f"{' '*space}{key.title().replace('_',' ')}: {value}", "", self.use_json), filehandle=self.fh)
    
    def print_metadata(self, metadata, dict_list, idx):
        for data, value in metadata.items():
            value = str(value).replace("\n", "\\n")
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"{data}{'.'*(30-len(data))}: {value}", "", self.use_json), filehandle=self.fh)
        ptmisclib.ptprint(ptmisclib.out_ifnot(self.check_if_next(dict_list, idx, 'metadata'), "", self.use_json), end="", filehandle=self.fh)

    def _find(self, page_content, re_pattern):
        """Find and return list of all occurences of *re_pattern* in *page_content*"""
        result = list(set(i for i in re.finditer(re_pattern, page_content)))
        result = list(set(result.group(0) for result in re.finditer(re_pattern, page_content)))
        if result and type(result[0]) == tuple:
            result = self.tuplelist_to_stringlist(result)
        result = list(set(result for result in result))
        return result

    def get_soup(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        bdos = soup.find_all("bdo", {"dir": "rtl"})
        for item in bdos:
            item.string.replace_with(item.text[::-1])
        return soup

    def rel2abs(self, url, domain):
        if not domain.endswith("/") and not url.startswith("/"):
            domain += "/"
        if url.startswith("http://") | url.startswith("https://") | url.startswith("ftp://") | url.startswith("ftps://") | url.startswith("irc://"):
            return url
        else:
            return domain + url

    def tuplelist_to_stringlist(self, tuplelist, num_tuple_part=False):
        stringlist = [] 
        for tup in tuplelist:
            if num_tuple_part:
                stringlist.append("".join(tup[num_tuple_part]))
            else:
                stringlist.append("".join(tup))
        return stringlist

    def get_forms(self, soup):
        """Returns parsed page forms"""
        allowed_elements = ["form", "input", "select", "textarea", "label", "button", "datalist", "output"]
        forms = soup.find_all("form") # Find all forms
        forms_result = []
        for form in forms:
            form_elements = self.strip_form_elements(form.find_all(allowed_elements))
            forms_result.append({"form_name": form.get("name"), "action": form.get("action"), "method": form.get("method"), "form_id": form.get("id"), 
            "inputs": [{"tag": ele.name, **ele.attrs} for ele in form_elements["inputs"]], "selects": [{"tag": ele.name, **ele.attrs} for ele in form_elements["selects"]]})

        return forms_result

    def strip_form_elements(self, form_elements):
        """strip child elements of parent element"""
        allowed_attrs = ("name", "type", "id", "value")
        result = {"inputs": [], "selects": []}
        for element in form_elements:
            element.attrs = {key: value for key, value in element.attrs.items() if key in allowed_attrs}
            if element.name == "select":
                element.attrs.update({"options": []})
            children = element.findChildren(True, recursive=True)
            for child in children:
                if child.name == "option":
                    element.attrs["options"].append(child.get("value", "notfound"))
                else:
                    child.unwrap()
            if element.name == "select":
                result["selects"].append(element)
            else:
                result["inputs"].append(element)
        return result

    def find_internal_parameters(self, internal_urls):
        parsed_urls = []
        for url in internal_urls:
            o = urllib.parse.urlsplit(url)
            if o.query:
                query_list = o.query.split("&")
                parsed_url = urllib.parse.urlunsplit((o[0], o[1], o[2], "", ""))
                result_data = {"url": parsed_url, "parameters": [query_list]}
                if not self.group_parameters:
                    parsed_urls.append(result_data)
                else:
                    if not parsed_urls:
                        parsed_urls.append(result_data)
                        continue
                    found = False
                    for d in parsed_urls:
                        if parsed_url == d["url"]:
                            d["parameters"].append(query_list)
                            found = True
                    if not found:
                        parsed_urls.append(result_data)
        return parsed_urls
    
    def get_domain(self, domain):
        if domain and not re.match("https?:\/\/", domain):
            ptmisclib.end_error("Scheme required in -d/--domain parameter", self.json_no, self.ptjsonlib, self.use_json)
        if domain and not domain.endswith("/"):
            domain += "/"
        return domain

    def get_url_list(self, args):
        try:
            url_list = self.read_file(args.file) if args.file else args.url
            url_list = list(dict.fromkeys(url_list))
            return url_list
        except FileNotFoundError:
            ptmisclib.end_error(f"File not found ({os.getcwd()})", self.json_no, self.ptjsonlib, self.use_json)

    def get_extract_types(self, extract_str):
        allowed_letters = {
            "E": "emails",
            "S": "subdomains",
            "H": "html_comments",
            "F": "forms",
            "L": "internal_urls",
            "X": "external_urls",
            "P": "phone_numbers",
            "M": "metadata",
            "I": "ip_addresses",
            "Q": "internal_urls_with_parameters",
            "A": "all"
        }
        extract_types = {
            "emails": None,
            "html_comments": None,
            "forms": None,
            "internal_urls": None,
            "external_urls": None,
            "internal_urls_with_parameters": None,
            "phone_numbers": None,
            "ip_addresses": None,
            "metadata": None,
            "subdomains": None, 
            "all": None,
        }
        for char in extract_str:
            if char in allowed_letters.keys():
                extract_types.update({allowed_letters[char]: True})
                if char == "A":
                    for i in extract_types:
                        extract_types[i] = True
                    break
            else:
                ptmisclib.end_error(f"Invalid parameter '{char}' in -e/--extract argument, allowed characters ({''.join(allowed_letters.keys())})", self.json_no, self.ptjsonlib, self.use_json)
        return extract_types

    def read_file(self, file):
        result = []
        with open(file, "r") as f:
            for line in f:
                line = line.strip("\n")
                x = re.compile(r"[\/]").split(line)
                if re.match('https?:\/\/', line):
                    result.append(line)
                elif self.domain:
                    if line.startswith("/"):
                        line = line[1:]
                    result.append(self.domain + line)
                else:
                    continue
            return result

def get_help():
    return [
        {"description": ["Script retrieves interesting information from web sources"]},
        {"usage": ["ptinsearcher <options>"]},
        {"usage_example": [
            "ptinsearcher -u https://www.example.com/",
            "ptinsearcher -u https://www.example.com/ -e H",
            "ptinsearcher -u https://www.example.com/ -e HSE",
            "ptinsearcher -f urlList.txt",
            "ptinsearcher -f urlList.txt -gc -e E",
        ]},
        {"options": [
            ["-u",  "--url",                   "<url>",            "Test URL"],
            ["-f",  "--file",                  "<file>",           "Load URL list from file"],
            ["-d",  "--domain",                "<domain>",         "Domain - Merge domain with filepath. Use when wordlist contains filepaths (e.g. /index.php)"],
            ["-e",  "--extract",               "<extract>",        "Specify types of data to extract [E, S, H, F, I, X, P, M, L, Q, A] (default A)"],
            ["-o",  "--output",                "<output>",         "Save output to file"],
            ["-op", "--output-parts",          "",                 "Save each extract_type to separate file"],
            ["-gp", "--group-parameters",      "",                 "Group parameters"], 
            ["-wp", "--without-parameters",    "",                 "Without parameters"],
            ["-g",  "--grouping",              "",                 "One output table for all sites"],
            ["-gc",  "--grouping-complete",    "",                 "Merge all results into one group"],
            ["-r",  "--redirect",              "",                 "Follow redirects (default False)"],
            ["-c",  "--cookie",                "<cookie=value>",   "Set cookie(s)"],
            ["-H",  "--headers",               "<header:value>",   "Set custom headers"],
            ["-p",  "--proxy",                 "<proxy>",          "Set proxy (e.g. http://127.0.0.1:8080)"],
            ["-ua", "--user-agent",            "<user-agent>",     "Set User-Agent (default Penterep Tools)"],
            ["-j",  "--json",                  "",                 "Output in JSON format"],
            ["-v",  "--version",               "",                 "Show script version and exit"],
            ["-h",  "--help",                  "",                 "Show this help message and exit"]
        ]
        }]                                                 


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, usage=f"{SCRIPTNAME} <options>")
    parser.add_argument("-u", "--url", type=str, nargs="+")
    parser.add_argument("-d", "--domain", type=str)
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-e", "--extract", type=str, default="A")
    parser.add_argument("-pd", "--post-data", type=str)
    parser.add_argument("-r", "--redirects", action="store_true")
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-op", "--output-parts", action="store_true")
    parser.add_argument("-g", "--grouping", action="store_true")
    parser.add_argument("-gc", "--grouping-complete", action="store_true")
    parser.add_argument("-gp", "--group-parameters", action="store_true")
    parser.add_argument("-wp", "--without-parameters", action="store_true")
    parser.add_argument("-p", "--proxy", type=str)
    parser.add_argument("-c", "--cookie", type=str, nargs="+")
    parser.add_argument("-H", "--headers", type=ptmisclib.pairs, nargs="+")
    parser.add_argument("-ua", "--user-agent", type=str, default="Penterep Tools")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}", help="show version")
    
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    args = parser.parse_args()
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptinsearcher"
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    args = parse_args()
    script = ptinsearcher(args)
    script.run()


if __name__ == "__main__":
    main()
