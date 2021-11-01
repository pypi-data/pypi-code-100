import os
from os import listdir
import pkg_resources


HTML_TEMPLATE_PATH = 'html_template'

html_templates = {}


class Html_bootstrap:
    """ Class to obtain html snippets in bootstrap format

	LONG DESCRIPTION OF CLASS

	ATTRIBUTES:
		ATTRIBUTE1(type): Description
		ATTRIBUTE2(type): Description
	"""

    def __init__(self, title = '', description = '', nav = '', footer = '', logo = ''):
        # Handles calling the ootstrap componenets required
        a = 1

        self.title = title
        self.description = description
        self.nav = nav
        self.footer_items = footer
        self.logo = logo

        if not html_templates:
            self.load_html_templates()

    def load_html_templates(self):

        files = pkg_resources.resource_listdir(__name__, HTML_TEMPLATE_PATH)

        # load html templates into memory
        for i in files:
            item = i.replace('.txt', '')
            filename = HTML_TEMPLATE_PATH + '/' + i
            
        
            html_templates[item] = pkg_resources.resource_string(__name__, filename)
            html_templates[item] = html_templates[item].decode("utf-8")
        return




    def heading(self, text, level = 'h1'):
        # Returns a heading with the inserted text
        # Level is leveh of heading (h1, h2)
        # Text is actual text to insert. 

        html_content = html_templates['heading']
        html_content = html_content.replace('{text}', text)
        html_content = html_content.replace('{level}', level)

        return html_content


    def text(self, text):
        # Return a paragraph

        return '<p>' + text + '</p>'


    def link(self, text, url):
        # Return a link
        html_content = html_templates['link']
        html_content = html_content.replace('{text}', text)
        html_content = html_content.replace('{url}', url)
        return html_content

    def image(self, contenturl): 

        if not contenturl:
            return ''

        content = '<img src="' + contenturl + '" class="img-fluid" alt="...">'
        return content


    def thumbnail(self, contenturl = '', linkurl = ''): 

        if not contenturl:
            return ''

        content = '<img src="' + contenturl + '" class="w-25" alt="...">'

        content = self.link(content, linkurl)

        return content


    def list(self, title, items, style_class_list = 'list-unstyled', style_class_item = ''):
        # Create list

        content = ''
        # Init list
        content += '<ul class="{style_class_list}">'.format(style_class_list = style_class_list)

        # Add items
        for i in items:
            content += '<li class="{style_class_item}">{item}</li>'.format(item = i, style_class_item=style_class_item)

        # Finalize list
        content += '</ul>'

        return content

    def breadcrumb(self, breadcrumb_items):
        # Returns breadcrumb html from list of url, text dicts.

        if not breadcrumb_items:
            return ''


        content = ''

        # Get past pages
        if len(breadcrumb_items) > 1:
            past_breadcrumb_items = breadcrumb_items[0:-1]

            for i in past_breadcrumb_items:
                url = i.get('url', '')
                text = i.get('text', '')

                content += '<li class="breadcrumb-item"><a href="{url}">{text}</a></li>'.format(url=url, text=text)

        # Get current pages
        record = breadcrumb_items[-1]
        url = record.get('url', '')
        text = record.get('text', '')
        content += '<li class="breadcrumb-item"><a href="{url}">{text}</a></li>'.format(url=url, text=text)


        html_content = html_templates['breadcrumb']
        html_content = html_content.replace('{breadcrumb_list}', content)
        return html_content


        return content

    def record(self, title = '', record = ''):
        # Return a web part for the record

        if not title: 
            title = ''


        # Build record
        record_content = ''
        for i in record:
            # Add key
            record_content +=  '<dt class="col-sm-3">'
            record_content +=  str(i) 
            record_content += ':</dt>'

            # Add values

            record_content += '<dd class="col-sm-9">'

            values = record.get(i, [])
            if not isinstance(values, list):
                values = [values]

            record_content += self.list('', values)

            record_content += '</dd>'


        # Build html

        base_content = html_templates['record']
        
        html_content = base_content.replace('{title}', title)

        html_content = base_content.replace('{record_content}', record_content)
        
        # Add title
        if title:
            title_content = self.heading(title)
            html_content = title_content + html_content
        
        
        return html_content




    def table(self, title, items, keys = []):
        # Returns a html table. Items are list of dicts. If keys is provided, only shows these columns. 

        # Get all keys from items if not provided
        if not keys:
            keys = []
            for i in items:
                for k in i:
                    keys.append(k)


        # Make header
        table_header = ''
        for i in keys:
            table_header += '<th scope="col">' + i + '</th>'
                    
        # MAke body
        table_body = ''
        for i in items:
            table_body += '<tr>'
            for k in keys:
                value = i.get(k, '')
                table_body += '<td>' + str(value) + '</td>'
      
            table_body += '</tr>'
      
        # Build table
        html_content = html_templates['table']
        html_content = html_content.replace('{table_header}', table_header)
        html_content = html_content.replace('{table_body}', table_body)
        return html_content



    def navbar(self, title, menu_items):
        # Returns a navbar

        if not title:
            title = ''

        # Build links
        list_items = []
        for i in menu_items:
            text = i.get('text', '')
            url = i.get('url', '')

            html_content = html_templates['navbar_item']
            html_content = html_content.replace('{url}', url)
            html_content = html_content.replace('{text}', text)
            list_items.append(html_content)


        # Convert links to list and assign style 'navbar-nav'
        menu_list_html = self.list('', list_items, 'navbar-nav', 'nav-item')

        html_content = html_templates['navbar']
        html_content = html_content.replace('{title}', title)
        html_content = html_content.replace('{menu_items}', menu_list_html)

        return html_content



    def footer(self, title, description, footer_items):
        # Returns a footer

        if not title:
            title = ''

        # Build links
        list_items = []
        for i in footer_items:
            text = i.get('text', '')
            link = i.get('link', '')

            list_items.append(self.link(text, link))

        # Convert links to list and assign style 'navbar-nav'
        footer_items_list_html = self.list('', list_items)


        html_content = html_templates['footer']
        html_content = html_content.replace('{title}', title)
        html_content = html_content.replace('{description}', description)

        html_content = html_content.replace('{footer_items}', footer_items_list_html)

        return html_content


    def article(self, title, image, content):
        # Returns an article web part
        
        page_content = ''
        page_content += self.heading(title)
        page_content += self.image(image)
        page_content += self.text(content)

        return page_content


    def page_blank(self, title, page_content, breadcrumb_items):

        # Returns a heading with the inserted text
        # Level is leveh of heading (h1, h2)
        # Text is actual text to insert. 

        if not title:
            title = ''


        nav_html = self.navbar(self.title, self.nav)
        
        page_footer_html = self.footer(self.title, self.description, self.footer_items)

        breadcrumb_html = self.breadcrumb(breadcrumb_items)

        html_content = html_templates['page']
        html_content = html_content.replace('{title}', title)
        html_content = html_content.replace('{nav}', nav_html)
        html_content = html_content.replace('{breadcrumb}', breadcrumb_html)

        html_content = html_content.replace('{content}', page_content)
        html_content = html_content.replace('{footer}', page_footer_html)

        return html_content


    def page_article(self, title, image, content, breadcrumb):
        # Returns a full web page including article web part

        body_content = self.article(title, image, content)
        
        return self.page_blank(title, body_content, breadcrumb)



    def card(self, image_url = '', link_url = '', title = '', text = ''):
        # Returns a card with the inserted text
        # Level is leveh of heading (h1, h2)
        # Text is actual text to insert. 

        html_content = html_templates['card']
        html_content = html_content.replace('{link_url}', link_url)
        html_content = html_content.replace('{card_title}', title)
        html_content = html_content.replace('{image_url}', image_url)
        html_content = html_content.replace('{card_text}', text)

        return html_content


    def cards(self, items):


        content = '<div class="row row-cols-1 row-cols-sm-4 g-4">'
        for item in items:

            content += '<div class="col">' + item + '</div>'
        content += '</div>'

        return content

    def section(self, title, content, expanded = False):
        # Expandable section
        
        # Remove non aascii characters for system title
        system_title = title.replace(' ', '')
        system_title = title.encode("ascii", "replace")
        system_title = 'section_' + system_title.decode("ascii", "replace").lower()
        system_title = title.replace(' ', '')


        # Convert true false in string
        js_expanded = str(expanded).lower()



        html_content = html_templates['section']
        
        html_content = html_content.replace('{title}', title)
        html_content = html_content.replace('{system_title}', system_title)
        html_content = html_content.replace('{content}', content)
        html_content = html_content.replace('{expanded}', js_expanded)

        return html_content


