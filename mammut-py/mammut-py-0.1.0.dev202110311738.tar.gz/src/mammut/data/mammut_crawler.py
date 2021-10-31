# coding=utf-8
import urllib.request as Request
from urllib.parse import urlparse
import urllib
from lxml import html, etree
import time


class CrawlingProperties:
    def __init__(self, base_url, nodes_pattern, node_elements, page_href = '', delay = 2, pagination_nodes_pattern = '',
                 pagination_element_xpath = '', pages_limit: int=None):
        self.base_url = base_url
        self.page_href = page_href
        self.nodes_pattern = nodes_pattern
        self.node_elements = node_elements
        self.delay = delay
        self.pagination_nodes_pattern = pagination_nodes_pattern
        self.pagination_element_xpath = pagination_element_xpath
        self.pages_limit = pages_limit

class MammutCrawler:
    """
    mammut crawler class
    """
    def __init__(self, crawling_properties: CrawlingProperties, update_status_text_box = None,  mammut_crawler = None):
        self.crawling_properties = crawling_properties
        self.update_status_text_box = update_status_text_box
        self.mammut_crawler = mammut_crawler

    def get_page(self, url):
        """
        return page string
        """
        req = Request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        request_response = Request.urlopen(req)
        page_string = request_response.read()
        return page_string

    def parse_string(self, page_tring):
        """
        lxml parsed string
        """
        page_lxml = html.fromstring(page_tring)
        return page_lxml

    def get_nodes(self, page_lxml, pattern):
        """
        elements that match pattern, return eTree objects as lists
        """
        nodes = page_lxml.xpath(pattern)
        return nodes

    def get_nodes_info(self, nodes, node_elements):
        """
        return information about the nodes like url,title or other to continue with crawling actions
        """
        nodes_info = []
        for node in nodes:
            nodes_info.append(self.get_node_data(node, node_elements))
        return nodes_info

    def get_node_data(self, node, node_elements):
        """
        nodeElemets serian un array de xpath relativos de las partes del articulo,receta,documento o lo que sea que se revise
        returns data of specified elements(xpaths) from one node
        """
        node_data = {}
        for elem in node_elements:
            node_data[elem] = self.get_node_element_data(node, node_elements[elem])
        return node_data

    def get_node_element_data(self, node, element_relative_path):
        """
        return data of a node, it need a relative path to the node to get the relevant data like: title, image, url, body...
        """
        data = ""
        try:
            if type(element_relative_path) == str:
                elem = node.xpath(element_relative_path)
                for i, j in enumerate(elem):
                    data = data + elem[i]
            else:
                data = element_relative_path
        except etree.XPathError:
            data = element_relative_path
        if data == '' and not element_relative_path.startswith('/'):
            data = element_relative_path
        return data

    def get_page_info(self, page_string, nodes_pattern, node_elements):
        parsed_page = self.parse_string(page_string)
        nodes = self.get_nodes(parsed_page, nodes_pattern)
        nodes_info = self.get_nodes_info(nodes, node_elements)
        return nodes_info

    def get_next_href(self, page_string, pagination_nodes_pattern, pagination_element_xpath):
        parsed_page = self.parse_string(page_string)
        pagination_nodes = self.get_nodes(parsed_page, pagination_nodes_pattern)
        if len(pagination_nodes) != 0:
            pagination_href_element = self.get_node_element_data(pagination_nodes[-1], pagination_element_xpath)
        else:
            pagination_href_element = ''
        if pagination_href_element != pagination_element_xpath and pagination_href_element[0] != '/':
            pagination_href_element = '/' + pagination_href_element

        return pagination_href_element

    def get_pages_info(self, test=False):
        next_href = self.crawling_properties.page_href
        all_nodes = []
        count = 0
        while True:
            time.sleep(self.crawling_properties.delay)
            # if next_href == self.crawling_properties.page_href:
            #     full_url = self.crawling_properties.base_url + next_href
            if next_href[0] == '/':
                url_path = urlparse(next_href[1:])
            else:
                url_path = urlparse(next_href)
            if url_path.netloc:
                full_url = url_path.geturl()
            else:
                #TODO: revisar esta logica del crawler, no funciona para bajar el corpus de degusta.
                # if next_href == self.crawling_properties.page_href:
                #     joined_path = urllib.parse.urljoin(urlparse(full_url).path, urlparse(next_href).path)
                # elif next_href[0] == '/':
                #     joined_path = urllib.parse.urljoin(urlparse(full_url).path, urlparse(next_href[1:]).path)
                # full_url = urllib.parse.urljoin(full_url, joined_path)
                full_url = urllib.parse.urljoin(self.crawling_properties.base_url, url_path.path)
            if self.update_status_text_box is not None:
                self.update_status_text_box()
            page_string = self.get_page(full_url)
            nodes_info = self.get_page_info(page_string, self.crawling_properties.nodes_pattern,
                                            self.crawling_properties.node_elements)
            for i in nodes_info:
                all_nodes.append(i)
            if self.crawling_properties.pagination_nodes_pattern != '' and self.crawling_properties.pagination_element_xpath != '':
                next_href = self.get_next_href(page_string, self.crawling_properties.pagination_nodes_pattern,
                                               self.crawling_properties.pagination_element_xpath)
            else:
                next_href = ''
            if not next_href.startswith('/'):#TODO: esta condicion garantiza que no es un url???
                break
            if test:
                break
            if self.crawling_properties.pages_limit - 1 == count:
                break
            count += 1
        return all_nodes

    def execute(self, test=False):
        all_of_all_data = []
        current_level_crawling_results = self.get_pages_info(test=test)
        if self.mammut_crawler == None:
            return current_level_crawling_results
        else:
            if test:
                current_level_crawling_results = current_level_crawling_results[:2]
            for index, i in enumerate(current_level_crawling_results):
                self.mammut_crawler.crawling_properties.page_href = i[list(i)[0]]
                page_info = self.mammut_crawler.execute(test=test)
                all_of_all_data = all_of_all_data + page_info
        return all_of_all_data
