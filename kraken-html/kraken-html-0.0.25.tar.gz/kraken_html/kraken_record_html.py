import copy
import json

class Kraken_record_html:
    # Converts normal schema record to html usable record

    def __init__(self, record):

        self.record = record


    @property
    def valid(self):
        # Test if valid record

        if not isinstance(self.record, dict):
            return False

        if not self.record_type:
            return False

        if not self.record_id:
            return False

        return True



    @property 
    def record_type(self):
        # Return record type

        #Error handling
        if not isinstance(self.record, dict):
            return None

        # Process
        return self.record.get('@type', '')


    @property
    def record_id(self):
        # Return record type

        #Error handling
        if not isinstance(self.record, dict):
            return None
        
        #Process
        return self.record.get('@id', '')


    @property
    def url(self): 
        # Return relative url for the record

        # Build url
        url = '/' + self.record_type + '/' + self.record_id

        return url


    @property
    def headline(self):
        return self._get_subrecord_attr('schema:headline', 'link')

    @property
    def author(self):
        return self._get_subrecord_attr('schema:headline', 'link')

    @property
    def articlebody(self):
        return self._get_subrecord_attr('schema:articlebody', 'link')

    @property
    def email(self):
        return self._get_subrecord_attr('schema:email', 'link')




    @property
    def name(self):
        # Gets the name of the record base don type and availability

        name = self.record.get('schema:name', None)
        email = self.record.get('schema:email', None)
        headline = self.record.get('schema:headline', None)


        if self.record_type == 'schema:article' and headline:
            record_name = headline
        elif name:
            record_name = name
        elif self.record_type == 'schema:person' and email:
            record_name = email
        else:
            record_name = self.record_id

        # If list, take first item
        if isinstance(record_name, list):
            record_name = record_name[0]

        return record_name

    @property
    def link(self):
        # Generate html link

        link = '<a href="{url}">{name}</a>'.format(url=self.url, name = self.name)
        
        return link

    @property
    def link_thumbnail(self):
        # Generate html link

        link = '<a href="{url}">{name}</a>'.format(url=self.url, name = self.name)
        
        return link


    @property
    def image(self):
        # Retrieves the url for the media picture
        # Priority:
        # thumbnail, content

        # Error handling
        if not isinstance(self.record, dict):
            return None


        record_thumbnailurl = self.record.get('schema:thumbnailurl', None)
        record_contenturl = self.record.get('schema:contenturl', None)
        record_image = self.record.get('schema:image', None)


        # Assign picture
        if record_thumbnailurl:
            picture_url = record_thumbnailurl
        elif record_contenturl:
            picture_url = record_contenturl
        else:
            picture_url = record_image

        if isinstance(picture_url, list):
            picture_url = picture_url[0]


        return picture_url


    @property
    def html_record(self, thumbnail = True):
        # Return record with sub-records as html links
        # Thumbnail flag activate / deactivate adding thumbnail

        # Create a copy so not to change original
        record = copy.deepcopy(self.record)
        new_record = {}

        # Loop through keys
        for i in record:

            # Convert to list
            if not isinstance(record[i], list):
                record[i] = [record[i]]

            # Iterate through list
            values = []
            for t in record[i]:

                # Test if valid record
                k = Kraken_record_html(t)
                if k.valid: 
                    value = k.link
                else:
                    value = t

                values.append(value)
            

            # Convert back to single item if needed. 
            if len(values) == 1:
                values = values[0]


            new_record[i] = values

        return new_record


    @property
    def layout(self):
        # Returns the page layout to use based on the record type

        if self.record_type in ['schema:article']:

            return 'article'

        elif self.record_type in ['schema:product']:

            return 'product'

        elif self.record_type in ['schema:imageobject']:

            return 'image'

        else:

            return 'record'


    @property 
    def jsonld(self):
        # Takes a record and returns a <scripys> jsonld type html code 
        
        schema_text = json.dumps(self.record, default=str, indent = 4)

        content = '\n<script type="application/ld+json">\n' + schema_text + '\n</script>\n'


        return content

    def _get_subrecord_attr(self, key, attr = None):
        # Retrieves a given fields from a sub-record. Returns list of values if several sub records

        sub_records = self.record.get(key, '')

        if not isinstance(sub_records, list):
            sub_records = [sub_records]

        values = []
        for i in sub_records:
            sub_kr = Kraken_record_html(i)
            if attr and sub_kr.valid:
                value = getattr(sub_kr, attr)
            else: 
                value = i

            values.append(value)

        # De list if needed
        if len(values) == 1:
            values = values[0]

        return values