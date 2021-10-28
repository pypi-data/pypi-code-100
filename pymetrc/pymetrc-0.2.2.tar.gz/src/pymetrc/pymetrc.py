from datetime import datetime, timedelta
import urllib.parse
import json
import os
from .apicaller import APICaller

# Currently only utilizing the Montana state Metrc API. Future plans include ability to choose endpoint in a more
# effective manner.
ENDPOINTS_FILE = os.path.join(os.path.dirname(__file__), 'endpoints.json')


class Metrc:
    '''
    A class to represent a Metrc client object. Contained within is a both a vendor API key and a unique user API key
    required for authentication with the Metrc REST API service. This allows for segmentation if using with multiple
    keys which may be necessary for a variety of reasons.

    Parameters
    ----------
    vendor_api_key : str
        Software vendor API key provided by Metrc upon validating that correct queries can be made.
    user_api_key : str
        API key tied to an individual which allows for access control and permissions for various subsets of related
        tasks within the state traceability system.
    state : str
        Two-letter state abbreviation for loading correct endpoints.

    Attributes
    ----------
    endpoints : dict
        Contains endpoint type (key) and a list of the associated endpoint url stubs (value). Several contain "{id}"
        which is modified via a string replace method to insert individual IDs.
    vendor_api_key : str
        Description in Parameters section above.
    user_api_key : str
        Description in Parameters section above.
    facility_data : list[dict]
        Facilities and all associated information as returned via the API.
    facilities : list[str]
        Facilities parsed from facility_data for easy access.
    dispensaries : list[str]
        Facilities that are identified as dispensaries.
    mipps : list[str]
        Facilities that are identified for manufacturing and processing.
    providers : list[str]
        Facilities that are identified as cultivators.
    '''

    def __init__(self, vendor_api_key, user_api_key, state):
        self.endpoints = self.load_endpoints(state)
        self.api_base_url = self.endpoints['base_url'][0]

        self.vendor_api_key = vendor_api_key
        self.user_api_key = user_api_key
        self.api = APICaller(self.vendor_api_key, self.user_api_key)
        self.init_facilities()

    def load_endpoints(self, state):
        '''
        Load the endpoints.json file and select endpoints from the state specified.

        Parameters
        ----------
        state : str
            Two-letter state abbreviation.

        Returns
        -------
        dict
            Dictionary of endpoint names as keys, URL endpoint stub as value.
        '''
        with open(ENDPOINTS_FILE, 'r') as f:
            data = json.load(f)
        return data[state]

    def init_facilities(self):
        '''
        Get and store facility data from Metrc. Additionally, create several facility-type specific lists for updating
        information relevant only to that specific type (i.e. sales transactions for dispensaries).
        '''
        print('Initializing facility list...')
        self.facility_data = self.get_basic('facilities_v1')

        self.facilities = [facility['License']['Number'] for facility in self.facility_data]

        # List all dispensaries using the boolean property in the facility data, CanSellToPatients.
        self.dispensaries = [facility['License']['Number'] for facility in self.facility_data
                             if facility['FacilityType']['CanSellToPatients']]

        # List all manufacturing licenses using the boolean property in the facility data, CanInfuseProducts.
        self.mipps = [facility['License']['Number'] for facility in self.facility_data
                      if facility['FacilityType']['CanInfuseProducts']]

        # List all provider licenses using the boolean property in the facility data, CanGrowPlants.
        self.providers = [facility['License']['Number'] for facility in self.facility_data
                          if facility['FacilityType']['CanGrowPlants']]

    def get_user_id(self):
        '''
        Return the fist seven (7) digits of the user API key. This can be used for creating unique database files,
        Elasticsearch indicies, etc. for each user/provider.

        Returns
        -------
        str
            First seven (7) characters of the user API key.
        '''
        return self.user_api_key[0:7]

    def get_facility_start_date(self, facility):
        '''
        Return the start date of the provided facility in ISO 8601 format (All praise the sanity of 8601). The start
        date is when the facility's state has blessed it as valid and legally allowed to operate. This can be used when
        obtaining records from "the beginning of time" from the persepective of that facility. For example, when
        initializing a database of all sales transactions, use the facility start date as the last modified start date.

        Many inconsistencies exist with the Metrc REST API. The first we'll note here -- start dates are provided as a
        calendar date. This is unacceptable. To provide them a helping hand, we append a time and offset string to make
        this useful for direct use in queries and for my own sanity.

        Parameters
        ----------
        facility : str
            The facility for which to fetch the start date.

        Returns
        -------
        str
            Facility start date.
        '''
        try:
            assert(facility in self.facilities)
        except AssertionError:
            print(f"Facility {facility} not available.")
            return None

        for f in self.facility_data:
            if f['License']['Number'] == facility:
                start_date = f['License']['StartDate']
                start_date += 'T00:00:00+00:00'
                break

        return start_date

    def get_24_hour_periods(self, start_date, end_date):
        '''
        Using a start and end datetime string in ISO 8601 format, return a list of tuples each representing no greater
        than 24 hours. The total of the periods returned will span the range provided. Metrc requires that, for time-
        based queries, each request covers a maximum of 24 hours. The end dates returned in the tuple are millisecond
        resolution -- we subtract one (1) millisecond to avoid overlap of an end date and the following start date and
        thus eliminate edge-case duplicate data. Timezone offsets can be different.

        Parameters
        ----------
        start_date: str
            Start date in ISO 8601 format (e.g. 2021-10-01T21:49:00+06:00)
        end_date: str
            End date in ISO 8601 format (e.g. 2021-10-17T05:19:32+06:00)

        Returns
        -------
        list[tuple(str, str)]
            Each tuple contains a datetime range that does not exceed 24 hours as strings in ISO 8601 format.
        '''
        try:
            # Verify the strings passed are ISO 8601 format and that the end date is greater than the start date.
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            assert((end_dt - start_dt).total_seconds() >= 0)
        except AssertionError:
            print("End date must be greater than start date.")
        except ValueError:
            print("One or more dates not in valid ISO format.")

        period_tuples = []

        while(1):
            # Calculate the difference in hours between the start and end date.
            difference = end_dt - start_dt
            difference = difference.total_seconds() / 3600

            if difference > 24:
                # Use the counter to create increments of < 24 hours. In this case, we subtract 1 millisecond to avoid
                # overlap when calculating subsequent 24 hour periods.
                end_date_counter = (start_dt + timedelta(days=1)) - timedelta(milliseconds=1)
                period_tuples.append((start_dt.isoformat(), end_date_counter.isoformat()))
                start_dt += timedelta(days=1)
            else:
                # If the original start and end represent a period of 24 hours or less, no modification is necessary.
                # This is also true when arriving at the end of the datetime iteration process above.
                period_tuples.append((start_dt.isoformat(), end_dt.isoformat()))
                break

        return period_tuples

    def get_basic(self, endpoint, license_number=None):
        ep = self.endpoints[endpoint][0]
        if license_number:
            url = f"{self.api_base_url}{ep}/?licenseNumber={license_number}"
        else:
            url = f"{self.api_base_url}{ep}"
        data = self.api.get_from_url_list([url])[0]
        return data

    def get_last_modified(self, endpoint, license_number, last_modified_start, last_modified_end, **kwargs):
        '''
        Retreive entities from an endpoint using last modified query parameters and flatten the list of lists of dicts.
        Return a straight list of entities represented as dictionary objects (e.g. list[package1, package2, package3]).

        Parameters
        ----------
        endpoint : str
            Endpoint/category of endpoints defined in the class attribute, endpoints (dict). For example, "packages"
            includes both active and inactive endpoints.
        license_number : str
            Facility license number to insert in query. User must have appropriate permissions for this facility granted
            in Metrc to obain valid data.
        last_modified_start : str
            Beginning of time range for the overall query in ISO 8601 format.
        last_modified_end : str
            End of time range for the overall query in ISO 8601 format.
        flatten : bool, optional
            Optional keyword argument for flattening any subdictionaries in the retrieved entities.

        Returns
        -------
        data : list[dict]
            Dictionary objects representing the target entity being requested.
        '''
        try:
            assert(license_number in self.facilities)
        except AssertionError:
            print('Invalid license: User must have access to facility.')

        self._print_get_message(endpoint, license_number, last_modified_start, last_modified_end)

        if endpoint == 'sales_v1_transactions':
            return self.get_sales_transactions(license_number=license_number,
                                               sales_date_start=last_modified_start,
                                               sales_date_end=last_modified_end,
                                               **kwargs)

        urls = self._generate_last_modified_urls(endpoint, license_number, last_modified_start, last_modified_end)
        response = self._get_from_urls(urls)
        data = [entity for period in response if period for entity in period]

        if kwargs.get('flatten'):
            return self._flatten_subdictionaries(data)
        else:
            return data

    def get_ids(self, endpoint, license_number, ids):
        '''
        Retreive entities from an ID based endpoint. These return a single dictionary each, so the concurrent API calls
        ultimately provide a list of dicts with no flattening necessary.

        Parameters
        ----------
        endpoint : str
            Endpoint/category of endpoints defined in the class attribute, endpoints (dict).
        license_number : str
            Facility license number to insert in query. User must have appropriate permissions for this facility granted
            in Metrc to obain valid data.
        ids : list[str]
            IDs to insert in the endpoint or otherwise target in the query.

        Returns
        -------
        data : list[dict]
            Dictionary objects representing the target entity being requested.
        '''
        try:
            assert(license_number in self.facilities)
        except AssertionError:
            print('Invalid license: User must have access to facility.')

        print(f'Getting {len(ids)} {endpoint}...')
        urls = []

        for ep in self.endpoints[endpoint]:
            for i in ids:
                query_dict = {'licenseNumber': license_number}
                query = urllib.parse.urlencode(query_dict)
                ep_with_id = ep.replace('{id}', str(i))
                urls.append(f"{self.api_base_url}{ep_with_id}?{query}")

        data = self._get_from_urls(urls)
        return data

    def get_sales_transactions(self, license_number, sales_date_start=None, sales_date_end=None, receipt_ids=None,
                               flatten=False):
        '''
        Get a list of transactions for a provided list of receipt IDs, or use a sales datetime range to first trigger a
        sales receipt lookup. This is an ID based query, so we must first get the list of valid IDs from the time-based
        endpoint, sales_receipts. If we do not provide a list of receipt IDs, the sales date start/end is required and
        vice versa.

        Note: At the time of this writing, the GET sales receipt endpoint is broken returning a status 500 when
        attempting to query by last modified start/end, or otherwise ignores the query parameters and defaults to the
        last 24 hours.

        Parameters
        ----------
        license_number : str
            Facility license number to query. User must have appropriate permissions for this facility granted in Metrc
            to obain valid data.
        sales_date_start : str, optional with IDs
            The start of the time range to query.
        sales_date_end : str, optional with IDs
            The end of the time range to query.
        receipt_ids : list[str], optional with sales date start/end
            IDs to lookup for transaction information.
        flatten : bool, default=False
            By default, transactions are identical to the recipt objects provided by the sales receipt endpoints except
            the transaction field contains a populated list of individual packages that were transacted from. If
            flattened, use the objects representing each single affected package and expand it to contain relevant
            information for the enclosing receipt ID.

        Returns
        -------
        list[dict]
            A list of receipt objects represented as dictionaries.
        '''
        try:
            assert(license_number in self.facilities)
        except AssertionError:
            print('Invalid license: User must have access to facility.')

        if not receipt_ids:
            try:
                assert(sales_date_start)
                assert(sales_date_end)
            except AssertionError:
                print('No receipt IDs provided: start and end date required.')

            print('No IDs provided when getting transactions...')
            receipts = self.get_last_modified('sales_v1_receipts_active', license_number, sales_date_start, sales_date_end)
            receipt_ids = [receipt['Id'] for receipt in receipts if isinstance(receipt, dict)]
            if not receipt_ids:
                print("No receipts in time period specified. Skipping transaction lookup.")
                return []

        transactions = self.get_ids('sales_v1_receipts_id', license_number, receipt_ids)

        # Flattening is useful for use in flat files, single database tables, and Elasticsearch indicies. Otherwise, the
        # returned dictionary includes a sub-list of transactions.
        if flatten:
            print('Flattening transactions...')
            flattened_transactions = []

            # Extract relevant information that would otherwise not be included when isolating an individual
            # transaction and append it.
            for receipt in transactions:
                receipt_info = {
                    'ReceiptNumber': receipt['ReceiptNumber'],
                    'SalesDateTime': receipt['SalesDateTime'],
                    'SalesCustomerType': receipt['SalesCustomerType'],
                    'PatientLicenseNumber': receipt['PatientLicenseNumber'],
                    'IsFinal': receipt['IsFinal'],
                    'ArchivedDate': receipt['ArchivedDate'],
                    'RecordedDateTime': receipt['RecordedDateTime'],
                    'RecordedByUserName': receipt['RecordedByUserName'],
                    'ReceiptLastModified': receipt['LastModified']
                }

                for transaction in receipt['Transactions']:
                    transaction.update(receipt_info)
                    flattened_transactions.append(transaction)

            return flattened_transactions
        else:
            return transactions

    def _print_get_message(self, endpoint, license_number, start_date, end_date):
        print(f'Getting {endpoint} for {license_number} between {start_date} and {end_date}')

    def _flatten_subdictionaries(self, entities):
        '''
        Process a list of entities, such as packages, and flatten any sub-dictionaries contained within. If a
        sub-dictionary is found, it is removed and we concatenate the name of the top-level key with the sub-key and
        assign it the sub-value. The entity is updated with the newly flattened key-value pairs.

        e.g. {'A': 'string', 'B': {'1': 'x', '2': 'y', '3': 'z'}} -> {'A': 'string', 'B1': 'x', 'B2': 'y', 'B3': 'z'}

        Parameters
        ----------
        entities : list[dict]
            List of entities represented as dictionaries.

        Returns
        -------
        list[dict]
            List of entites represented as dictionaries with sub-dictionary values flattened.
        '''
        print('Flattening objects...')
        flattened_entities = []

        for entity in entities:
            keys_to_flatten = []
            for key, value in entity.items():
                if isinstance(value, dict):
                    keys_to_flatten.append(key)

            for key in keys_to_flatten:
                value = entity.pop(key)
                new_value = {}

                for subkey, subvalue in value.items():
                    cat_key = key + subkey
                    new_value.update({cat_key: subvalue})

                entity.update(new_value)
            flattened_entities.append(entity)

        return flattened_entities

    def _get_from_urls(self, urls):
        '''
        Take a list of urls and pass them to the APICaller, getting back a list of responses in dictionaries. To be
        precise, we get back a list of lists of dictionaries, i.e.:

          |--------- 24 hr period ---------|  |--------- 24 hr period ---------|  |- 24 hr period -|
        [ [ { package: 1 }, { package: 2 } ], [ { package: 3 }, { package: 4 } ], [ { package: 5 } ] ]

        The above example assumes we have made a request from the packages endpoint for packages last modified within
        three (3) 24 hour periods. Since we get the JSON data back converted to a Python dictionary object, and we must
        make a separate call for each 24 hour period, we get a list of lists of dictionaries.

        As many requests can be required, either for time-based queries or for ID-based queries such as when first
        initializing your database, this is done concurrently using AIOHTTP.

        Parameters
        ----------
        urls: list[str]
            URLs from which to make get requests.

        Returns
        -------
        list[list[dict]]
            The outer list contains all individual endpoint queries. The inner list contains all the entities returned
            an individual endpoint query. The dict is the dictionary representing the JSON object returned.
        '''
        response_json = self.api.get_from_url_list(urls)
        return response_json

    def _generate_last_modified_urls(self, endpoint, license_number, last_modified_start, last_modified_end):
        '''
        Create a list of URLs for endpoint accepting queries based on last-modified datetimes (e.g. packages, harvests).

        Parameters
        ----------
        endpoint : str
            Endpoint/category of endpoints defined in the class dict attribute, endpoints. For example, "packages"
            includes both active and inactive endpoints.
        license_number : str
            Facility license number to insert in query. User must have appropriate permissions for this facility
            granted in Metrc to obain valid data.
        last_modified_start : str
            Beginning of time range for the overall query in ISO 8601 format.
        last_modified_end : str
            End of time range for the overall query in ISO 8601 format.

        Returns
        -------
        list[str]
            A list of crafted URLs to be used for querying the Metrc API.
        '''
        date_ranges = self.get_24_hour_periods(last_modified_start, last_modified_end)
        urls = []

        # Note: At the time of this writing, the GET sales receipt endpoint is broken returning a status 500 when
        # attempting to query by last modified start/end, or otherwise ignores the query parameters and defaults to the
        # last 24 hours.
        if endpoint == 'sales_v1_receipts_active':
            query_start_term = 'salesDateStart'
            query_end_term = 'salesDateEnd'
        else:
            query_start_term = 'lastModifiedStart'
            query_end_term = 'lastModifiedEnd'

        for ep in self.endpoints[endpoint]:
            for period in date_ranges:
                query_dict = {'licenseNumber': license_number,
                              query_start_term: period[0],
                              query_end_term: period[1]}
                query = urllib.parse.urlencode(query_dict)
                urls.append(f"{self.api_base_url}{ep}?{query}")

        return urls


if __name__ == '__main__':
    import os

    vendor_api_key = os.environ['METRC_VENDOR_API_KEY']
    user_api_key = os.environ['METRC_USER_API_KEY']
    m = Metrc(vendor_api_key, user_api_key, 'mt')
