
from kraken_html.html_bootstrap import Html_bootstrap as HTMLBOOT
from kraken_html.kraken_record_html import Kraken_record_html as KR_HTML
import pkg_resources


import json
import requests

#from models.html_form import Html_form

# These lines ensure fiels are retrievable once packaged as a library

CONTENT_TEMPLATE = 'content_template/'

class Kraken_html:
    """ Class to generate html pages based on standard kraken records

    Attributes:
    - get_page: Gets a full website page with default record page layout
    - 

    Parts:
    - get_article: 
    - get_product:
    - get_record:
    - get_image
    - get_video


    """

    def __init__(self, organization = '', title = None, description = '', nav = '', footer_nav = '', logo = ''):


        self.organization = organization
        self.title = title
        self.description = description
        self.nav = nav
        self.footer_nav = footer_nav
        self.logo = logo

        self.html = HTMLBOOT(self.title, self.description, self.nav, self.footer_nav, self.logo)

        """
        config_file = {
            'organization': 'Org name',
            'title': 'Title of website',
            'description': 'Some description of the website',
            'nav': [
                {'url': '/home', 'text': 'Home'},
                {'url': '/products', 'text': 'Products'},
                {'url': '/about', 'text': 'About us'},
                {'url': '/contact', 'text': 'Contact us'}
                ],
            'footer_nav': [
                {'url': '/privacy', 'text': 'Privacy policy'},
                {'url': '/terms', 'text': 'Terms'},
                {'url': '/about', 'text': 'About us'},
                {'url': '/contact', 'text': 'Contact us'}
                ],
            'logo': 'https://cdn.icon-icons.com/icons2/1678/PNG/512/wondicon-ui-free-home_111275.png',
            'read_db': 'https://storage.googleapis.com/krkn/v1'
            }
        """
        


    def config(self, config_record):

        self.organization = config_record.get('organization', '')
        self.title = config_record.get('title', '')
        self.description = config_record.get('description', '')
        self.nav = config_record.get('nav', '')
        self.footer_nav = config_record.get('footer_nav', '')
        self.logo = config_record.get('logo', ''),
        self.read_db = config_record.get('read_db', '')

        self.html = HTMLBOOT(self.title, self.description, self.nav, self.footer_nav, self.logo)
        
    def get_db_record(self, record_type, record_id):
        # Retrieves a record from kraken db

        url = self.read_db + '/' + record_type + '/' + record_id + '.json'

        try:
            r = requests.get(url)

            record = json.loads(r.content)

        except:
            print(r.content)
            record = None

        return record


    def get_records_page(self, records, breadcrumbs = ''):
        # Shows page with multiple record

        title = 'Title'

        schema_content = ''


        records_content = self.get_cards(records)

        # Combine parts
        body_content = schema_content + records_content 


        # Insert in web page
        page_content = self.html.page_blank(title, body_content, breadcrumbs)


        return page_content


    def get_record_page(self, record, breadcrumbs = ''):
        # Returns full web page with relevant web part for the record
        '''
        Page structure:
        - page_content:
            - jsonld_content
            - body_content:
                - part1_content
                - part2_content

        '''


        kr = KR_HTML(record)

        # If invalida record, send error message
        if not kr.valid:
            title = 'Invalid record'
            body_content = str(record)
            return self.html.page_blank(title, body_content, breadcrumbs)



        # Retrieve jsonld
        jsonld_content = kr.jsonld


        # Retrieve web part usinf proper record style

        if kr.layout == 'article':

            part_content = self.get_article(record, breadcrumbs)

        elif kr.layout == 'image':

            part_content = self.get_page_image(record, breadcrumbs)


        elif kr.layout == 'product':

            part_content = self.get_page_product(record, breadcrumbs)

        else:
            part_content = self.get_record(record, breadcrumbs)




        # Combine parts
        body_content = jsonld_content + part_content 


        # Insert in web page
        page_content = self.html.page_blank(kr.name, body_content, breadcrumbs)


        return page_content



    def get_article(self, record, breadcrumbs = ''):
        # Return a full page with article template html of the record
        '''
        article:
            - title
            - author
            - image
            - body text
        '''

        kr = KR_HTML(record)

        # Retrieve web part
        part_content = self.html.article(kr.headline + 'f', kr.image, kr.articlebody)

        return part_content


    def get_image(self, record, breadcrumbs = ''):
        # Return a full page with article template html of the record
        
        # Extarct relevant data from record
        title = record.get('schema:headline', '')
        articlebody = record.get('schema:articlebody', '')
        image = record.get('schema:image', '')

        return self.html.page_image(title, image, articlebody, breadcrumbs)

    def get_product(self, record, breadcrumbs = ''):
        # Return a full page with article template html of the record
        
        # Extarct relevant data from record
        title = record.get('schema:headline', '')
        articlebody = record.get('schema:articlebody', '')
        image = record.get('schema:image', '')

        return self.html.page_product(title, image, articlebody, breadcrumbs)
    

    def get_record(self, record, breadcrumbs = ''):
        # Return a full page with article template html of the record
        
        kr = KR_HTML(record)


        # Retrieve picture (if one)
        print(kr.image)
        image_content = self.html.thumbnail(kr.image)

        # Retrieve web part
        record_content = self.html.record(kr.name, kr.html_record)


        # Combine parts
        body_content = image_content + record_content 


        return body_content




    def get_cards(self, records):
        # Return html cards

        if not isinstance(records, list):
            records = [records]

        cards = []
        for i in records:
            kr = KR_HTML(i)
            image_url = kr.image
            link_url = kr.url
            name = kr.name

            cards.append(self.html.card(image_url, link_url, name))

        cards_html = self.html.cards(cards)

        return cards_html



    def get_record_template(self, page, language = 'en'):
        # Get file Name. 
        filename = CONTENT_TEMPLATE + page + '_' + language + '.json'

        # Load file

        content = pkg_resources.resource_string(__name__, filename)
        content = content.decode("utf-8")
        

        # COnvert \n to <br>
        content = content.replace('\\n', '<br>')


        # Change placeholders

        content = content.replace('{organization}',self.organization)



        # Convert to json
        record = json.loads(content)


        # Return
        return record





    def _get_keys(self, value):

        if not isinstance(value, list):
            value = [value]

        keys = []

        for i in value:
            for key in i:
                if key not in keys:
                    keys.append(key)

        return sorted(keys)

