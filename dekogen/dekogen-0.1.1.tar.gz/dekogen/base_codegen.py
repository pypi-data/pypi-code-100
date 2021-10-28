"""Provides ability to generate simple python code"""
from dekogen.file_writer import NEW_LINE

BASE_INDENT = '    '


class CodeGenerator:
    """Utility class to generate code items method, class etc."""

    @staticmethod
    def gen_class(class_name, inner_methods, inner_properties=None, base_class=None):
        """
        Generate class sting
        :param class_name: Name of the class
        :param inner_properties: Class level properties
        :param inner_methods: Class methods
        :param base_class: Inheritance class
        :return: Class content string
        """
        class_template = 'class {name}{base}:{doc_string}{properties}{methods}'
        class_doc_template = '"""Describes {} definition via python code"""'

        base_class = '({})'.format(base_class) if base_class else ''
        inner_properties = NEW_LINE.join(['{0}{1}'.format(BASE_INDENT, line)
                                          for line in inner_properties]) if inner_properties else ''
        inner_methods = NEW_LINE.join(['{0}{1}{new_line}'.format(BASE_INDENT, line, new_line=NEW_LINE)
                                       if 'return' in line and method != inner_methods[-1]
                                       else '{0}{1}'.format(BASE_INDENT, line) for method in inner_methods for line in
                                       method if line])
        class_doc_sting = ''.join((BASE_INDENT, class_doc_template.format(class_name)))

        return class_template.format(name=class_name, base=base_class,
                                     doc_string='{new_line}{str}{new_line}{new_line}'
                                     .format(str=class_doc_sting, new_line=NEW_LINE) if class_doc_sting else '',
                                     properties='{str}{new_line}'
                                     .format(str=inner_properties, new_line=NEW_LINE) if inner_properties else '',
                                     methods='{str}{new_line}'
                                     .format(str=inner_methods, new_line=NEW_LINE) if inner_methods else '')

    @staticmethod
    def gen_method(method_name, method_body, parameters=None, doc_string=None):
        """
        Generate list of method lines
        :param method_name: Name of the method
        :param method_body: List of lines of the body content
        :param parameters: List method arguments
        :param doc_string: custom method docstring
        :return: Method content lines list
        """
        method_template = 'def {0}({1}):{new_line}{2}{new_line}{3}'
        method_doc = doc_string if doc_string else '"""Assigns values to corresponding fields"""'

        parameters = ', '.join(('self',) + tuple(parameters)) if parameters else 'self'
        method_body = ''.join(['{0}{1}{new_line}'.format(BASE_INDENT, line, new_line=NEW_LINE) for line in method_body])
        method_doc_string = ''.join((BASE_INDENT, method_doc))
        return method_template.format(method_name, parameters, method_doc_string, method_body,
                                      new_line=NEW_LINE).split(NEW_LINE)
