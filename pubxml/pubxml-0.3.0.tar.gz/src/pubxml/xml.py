from dataclasses import dataclass, field
from pathlib import Path
from lxml import etree


@dataclass
class XML:
    filename: str = None
    root: str = None
    tree: str = None
    nsmap: dict = field(default_factory=dict)

    def __post_init__(self):
        # If there's a filename and no root or tree, parse the file.
        # Otherwise, set the root and tree
        if self.filename and not self.tree and not self.root:
            self.tree = etree.parse(self.filename)
            self.root = self.tree.getroot()
        elif self.root:
            self.tree = self.root.getroottree()
        elif self.tree:
            self.root = self.tree.getroot()

        # If there's no nsmap given, generate the nsmap from the root element
        if not self.nsmap and self.root is not None:
            self.nsmap = {
                ns if ns is not None else '_': uri
                for ns, uri in self.root.nsmap.items()
            }

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(filename="{self.filename}", root="{self.root}")'
        )

    def write(self, filename=None, method='c14n', **kwargs):
        """
        Write the XML document to a file (using the XML.tree.write() method).

        * filename=None: An optional filename to write to (default=self.filename).
        * method='c14n': Canonicalize output by default.
        """
        self.tree.write(filename or self.filename, **kwargs)

    @property
    def path(self):
        """
        return a pathlib.Path object containing the document filename, or None
        """
        if self.filename is not None:
            return Path(self.filename)

    def xpath(
        self, expr, element=None, nsmap=None, extensions=None, strings='plain', **params
    ):
        """
        Return xpath results for the given context or document root.

        * expr: the xpath expression
        * element: the element context in which to evaluate the xpath expression
        * nsmap: the namespace map to use with the expression (default = Document nsmap)
        * extensions: additional xpath extension functions to make available
        * strings: default='plain' to return plain strings, 'smart' to use smart strings
          (smart strings have a `.getparent()` method). Smart strings are off by default
          for efficiency.
        * **params: additional parameters that are made available to xpath.
        """
        if not element:
            element = self.root
        xpath_args = {
            'namespaces': nsmap or self.nsmap,  # use the Document nsmap by default
            'extensions': extensions,
            'smart_strings': strings == 'smart',  # return 'plain'
            **params,
        }
        return element.xpath(expr, **xpath_args)

    def first(
        self, path, context=None, nsmap=None, exts=None, strings='plain', **params
    ):
        """
        Return first xpath result for the given context or document root, or None.
        """
        results = self.xpath(
            path, context=context, nsmap=nsmap, exts=exts, strings='plain', **params
        )
        return next(iter(results), None)

    def prefixed_tag(self, element, nsmap=None):
        nsmap = nsmap or self.nsmap
        tag = element.tag.split('}')[-1]
        if element.prefix:
            return f'{element.prefix}:{tag}'
        elif '}' in element.tag:
            ns = element.tag.split('}')[0].strip('{}')
            if nsmap and ns in nsmap.values():
                keys, values = list(nsmap.keys()), list(nsmap.values())
                prefix = keys[values.index(ns)]
                return f'{prefix}:{tag}'
        return tag