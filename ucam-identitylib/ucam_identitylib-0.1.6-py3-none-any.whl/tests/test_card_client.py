from unittest import TestCase
from base64 import b64encode
from requests import exceptions, Session
from requests_mock import Mocker
from typing import Mapping, Optional

from identitylib.card_client import CardClient
from identitylib.identifiers import IdentifierSchemes

CRSID_SCHEME = str(IdentifierSchemes.CRSID)


class TestCardParsingMethods(TestCase):

    card_with_all_ids = {
        'id': 'card-with-identifiers',
        'identifiers': [
            {'scheme': str(IdentifierSchemes.CRSID), 'value': 'wgd23'},
            {'scheme': str(IdentifierSchemes.USN), 'value': '300001'},
            {'scheme': str(IdentifierSchemes.STAFF_NUMBER), 'value': '1000'},
            {'scheme': str(IdentifierSchemes.BOARD_OF_GRADUATE_STUDIES), 'value': '5'},
            {'scheme': str(IdentifierSchemes.LEGACY_CARDHOLDER), 'value': 'aa000a1'},
            {'scheme': str(IdentifierSchemes.STUDENT_INSTITUTION), 'value': 'hh'},
            {'scheme': str(IdentifierSchemes.HR_INSTITUTION), 'value': ''},
            {'scheme': str(IdentifierSchemes.LEGACY_CARD_INSTITUTION), 'value': ''},
            {'scheme': str(IdentifierSchemes.STUDENT_ACADEMIC_PLAN), 'value': ''},
            {'scheme': str(IdentifierSchemes.CARD), 'value': ''},
            {'scheme': str(IdentifierSchemes.LEGACY_TEMP_CARD), 'value': ''},
            {'scheme': str(IdentifierSchemes.MIFARE_ID), 'value': '11201010'},
            {'scheme': str(IdentifierSchemes.MIFARE_NUMBER), 'value': '32424121479'},
            {'scheme': str(IdentifierSchemes.LEGACY_CARD), 'value': '1324352'},
            {'scheme': str(IdentifierSchemes.BARCODE), 'value': 've1212'},
            {'scheme': str(IdentifierSchemes.CARD_LOGO), 'value': ''},
            {'scheme': str(IdentifierSchemes.PHOTO), 'value': '1'},
            {'scheme': str(IdentifierSchemes.LEGACY_PHOTO), 'value': ''},
        ]
    }

    def test_get_identifier_by_scheme_can_find_all_ids(self):
        test_card = TestCardParsingMethods.card_with_all_ids

        for identifier_dict in test_card['identifiers']:
            scheme = identifier_dict['scheme']
            value = identifier_dict['value']

            self.assertEqual(
                CardClient.get_identifier_by_scheme(test_card, scheme),
                f'{value}@{scheme}'.lower()
            )

    def test_get_identifier_by_scheme_returns_none_for_no_matching_identifier(self):
        test_card = {'identifiers': []}

        for id_scheme in IdentifierSchemes.get_registered_schemes():
            self.assertIsNone(CardClient.get_identifier_by_scheme(test_card, id_scheme))


class CardAPITestMixin:
    """
    Mixin that provides convenience methods for constructing a card client and card client urls

    """

    base_url = 'https://card-api.com'

    @Mocker()
    def setUp(self, request_mocker: Mocker, config: Optional[Mapping] = {}):
        """
        Setup the card client here in order to intercept the initial auth request.

        """

        super(CardAPITestMixin, self).setUp()

        auth_request = request_mocker.post(
            'https://api.apps.cam.ac.uk/oauth/client_credential/accesstoken',
            json={
                'token_type': 'Bearer',
                'access_token': 'fake-token',
            }
        )

        self.client = CardClient('mock-client-id', 'mock-client-key', config=config)
        self.assertIsInstance(self.client.session, Session)

        self.assertEqual(len(auth_request.request_history), 1)
        self.assertEqual(
            auth_request.request_history[0].headers['Authorization'],
            f'Basic {b64encode(b"mock-client-id:mock-client-key").decode("utf-8")}'
        )


class TestGetCardsByIds(CardAPITestMixin, TestCase):

    mocked_cards = [{
        'id': 'card-1',
        'identifiers': [{'scheme': CRSID_SCHEME, 'value': 'wgd23'}]
    }, {
        'id': 'card-2',
        'identifiers': [{'scheme': CRSID_SCHEME, 'value': 'wgd23'}]
    }, {
        'id': 'card-3',
        'identifiers': [{'scheme': CRSID_SCHEME, 'value': 'wgd23'}]
    }]

    @Mocker()
    def test_card_cards_by_id_gives_an_iterator_of_each_card(self, request_mocker: Mocker):
        """
        Sanity test that the client can get cards by identifier - calling the correct
        endpoint and returning the identifiers as an iterator.
        """

        adapter = request_mocker.post(
            f'{self.client.base_url}/cards/filter/?page_size=200',
            json={'results': TestGetCardsByIds.mocked_cards, }
        )

        result = list(self.client.cards_for_identifiers(['wgd23', 'rjg21']))
        self.assertListEqual(result, TestGetCardsByIds.mocked_cards)

        # check that the identifiers were sent in the request
        self.assertEqual(adapter.last_request.json(), {'identifiers': ['wgd23', 'rjg21']})

    @Mocker()
    def test_id_requests_are_chunked_and_pages_followed(self, mocker):
        """
        Test that requests for large amounts of identifiers are chunked
        and that any paged responses are followed for these chunks

        """
        # create 55 ids, which is over the default chunk size for the number of ids that
        # will be sent with one request
        ids = [f'aa{index}' for index in range(55)]

        chunk_posts = mocker.post(
            f'{self.client.base_url}/cards/filter/?page_size=200', [{
                # initial post for the first chunk of ids - gives a 'next' link which should be
                # followed
                'json': {
                    'results': [TestGetCardsByIds.mocked_cards[0]],
                    'next': f'{self.client.base_url}/cards/filter/?cursor=aE02sMDIALx9',
                }
            }, {
                # the second post for the last chunk of ids
                'json': {
                    'results': [TestGetCardsByIds.mocked_cards[2]]
                }
            }])

        # the request to get the second page from the initial response
        chunk_one_paged_post = mocker.post(
            f'{self.client.base_url}/cards/filter/?cursor=aE02sMDIALx9',
            json={
                'results': [TestGetCardsByIds.mocked_cards[1]],
            }
        )

        result = list(self.client.cards_for_identifiers(ids))
        self.assertListEqual(result, TestGetCardsByIds.mocked_cards)

        # check that two chunked requests were made and the number of identifers sent in
        # each request was 50 and 5.
        self.assertEqual(len(chunk_posts.request_history), 2)
        self.assertEqual(chunk_posts.request_history[0].json(), {'identifiers': ids[:50]})
        self.assertEqual(chunk_posts.request_history[1].json(), {'identifiers': ids[50:]})

        # check that the page request was made without any body
        self.assertIsNone(chunk_one_paged_post.last_request.text)

    @Mocker()
    def test_id_chunk_size_can_be_amended(self, mocker):
        """
        Test that we can set a custom chunk size and id requests will be chunked by
        this size

        """

        # setup the request handler to respond with each id one at a time
        chunk_posts = mocker.post(
            f'{self.client.base_url}/cards/filter/?page_size=200',
            [{
                'json': {
                    'results': [TestGetCardsByIds.mocked_cards[0]],
                }
            }, {
                'json': {
                    'results': [TestGetCardsByIds.mocked_cards[1]],
                }
            }, {
                'json': {
                    'results': [TestGetCardsByIds.mocked_cards[2]],
                }
            }]
        )

        # make a request using tiny chunk size - we should get all cards back
        result = list(self.client.cards_for_identifiers(
            ['wgd23', 'rjg21', 'fjc55'], chunk_size=1)
        )
        self.assertListEqual(result, TestGetCardsByIds.mocked_cards)

        # assert that three requests have been made each with a single id
        self.assertEqual(len(chunk_posts.request_history), 3)
        self.assertEqual(chunk_posts.request_history[0].json(), {'identifiers': ['wgd23']})
        self.assertEqual(chunk_posts.request_history[1].json(), {'identifiers': ['rjg21']})
        self.assertEqual(chunk_posts.request_history[2].json(), {'identifiers': ['fjc55']})

    @Mocker()
    def test_params_are_applied_to_request(self, mocker):
        """
        Test that we can set a custom chunk size and id requests will be chunked by
        this size

        """

        # setup the request handler to expect additional query params - but respond with nothing
        mocker.post(
            f'{self.client.base_url}/cards/filter/?page_size=200&status=ISSUED&key=value',
            json={})

        # make a request with params - this would raise if we missed the url above
        result = list(self.client.cards_for_identifiers(['wgd23'], params={
            'status': 'ISSUED',
            'key': 'value'
        }))
        self.assertListEqual(result, [])


class TestGetAllCards(CardAPITestMixin, TestCase):

    mocked_cards = [
        {
            'id': f'card-{index}',
            'identifiers': [{'scheme': CRSID_SCHEME, 'value': f'aab{index}'}]
        }
        for index in range(300)
    ]

    @Mocker()
    def test_all_cards_can_be_fetched_with_pages(self, request_mocker: Mocker):
        """
        Test that all cards can be fetched and paged responses handled

        """

        # initial request which returns a next link
        request_mocker.get(
            f'{self.client.base_url}/cards/?page_size=200', json={
                'results': TestGetAllCards.mocked_cards[:200],
                'next': f'{self.client.base_url}/cards/?cursor=agrXdw32'
            })

        # the request to get the next link
        request_mocker.get(f'{self.client.base_url}/cards/?cursor=agrXdw32',
                           json={'results': TestGetAllCards.mocked_cards[200:]}
                           )

        response = list(self.client.all_cards())

        # we should have all cards
        self.assertListEqual(response, TestGetAllCards.mocked_cards)

    @Mocker()
    def test_query_params_can_be_applied(self, request_mocker: Mocker):
        """
        Test that query params can be passed into the method and applied to the query string

        """

        super(TestGetAllCards, self).setUp(config={'page_size': 750})

        # setup the request handler to expect additional query params - but respond with nothing
        request_params = '?page_size=750&status=REVOKED&card_type=MIFARE_TEMPORARY'
        request_mocker.get(
            f'{self.client.base_url}/cards/{request_params}',
            json={}
        )

        response = list(self.client.all_cards(
            {'status': 'REVOKED', 'card_type': 'MIFARE_TEMPORARY', 'page_size': 750}))

        # we should have no cards
        self.assertListEqual(response, [])

    @Mocker()
    def test_page_size_can_be_altered(self, request_mocker):
        """
        Test that we can set a custom page size which is used in the query params of the
        request to the Card API

        """
        super(TestGetAllCards, self).setUp(config={'page_size': 500})

        request_mocker.get(
            f'{self.client.base_url}/cards/?page_size=500',
            json={
                'results': TestGetAllCards.mocked_cards,
            })

        response = list(self.client.all_cards({'page_size': 500}))

        # we should have all cards
        self.assertListEqual(response, TestGetAllCards.mocked_cards)


class TestGetCardDetail(CardAPITestMixin, TestCase):

    @Mocker()
    def test_get_card_detail_returns_record(self, request_mocker: Mocker):
        """
        Test that get card detail calls the right endpoint and returns the json from the API

        """

        request_mocker.get(
            f'{self.client.base_url}/cards/test-card-id/',
            json={
                'id': 'test-card-id',
                'identifiers': [],
                'issuedAt': '2000-01-23T00:00:00Z',
                'issueNumber': 1,
                'expiresAt': '2001-01-31T00:00:00Z',
                'status': 'EXPIRED',
                'cardType': 'MIFARE_PERSONAL',
                'notes': []
            }
        )

        card_detail = self.client.get_card_detail('test-card-id')

        self.assertEqual(card_detail, {
            'id': 'test-card-id',
            'identifiers': [],
            'issuedAt': '2000-01-23T00:00:00Z',
            'issueNumber': 1,
            'expiresAt': '2001-01-31T00:00:00Z',
            'status': 'EXPIRED',
            'cardType': 'MIFARE_PERSONAL',
            'notes': []
        })

    @Mocker()
    def test_get_card_detail_errors_are_raised(self, request_mocker: Mocker):
        """
        Test that http errors are raised if the underlying request fails

        """

        request_mocker.get(
            f'{self.client.base_url}/cards/no-such-card-id/',
            exc=exceptions.HTTPError('404 Not Found')
        )

        with self.assertRaises(exceptions.HTTPError):
            self.client.get_card_detail('no-such-card-id')


class TestPageSize(CardAPITestMixin, TestCase):

    mocked_cards = [{
        'id': 'card-1',
        'identifiers': [{'scheme': CRSID_SCHEME, 'value': 'wgd23'}]
    }, {
        'id': 'card-2',
        'identifiers': [{'scheme': CRSID_SCHEME, 'value': 'wgd23'}]
    }, {
        'id': 'card-3',
        'identifiers': [{'scheme': CRSID_SCHEME, 'value': 'wgd23'}]
    }]

    @Mocker()
    def test_page_size_is_honored_and_pages_followed(self, request_mocker):
        """
        Test that the client sends the page size as setup in __init__
        and that pages are followed when a paged response is given

        """

        super(TestPageSize, self).setUp(config={'page_size': 1})

        initial_post = request_mocker.post(
            f'{self.client.base_url}/cards/filter/?page_size=1',

            json={
                'results': [TestGetCardsByIds.mocked_cards[0]],
                'next':
                f'{self.client.base_url}/cards/filter/?cursor=cD0yMDIxL',
            })

        page_two_post = request_mocker.post(
            f'{self.client.base_url}/cards/filter/?cursor=cD0yMDIxL',
            json={
                'results': [TestGetCardsByIds.mocked_cards[1]],
                'next':
                f'{self.client.base_url}/cards/filter/?cursor=efSx21sf3L',
            })

        page_three_post = request_mocker.post(
            f'{self.client.base_url}/cards/filter/?cursor=efSx21sf3L',
            json={'results': [TestGetCardsByIds.mocked_cards[2]]}
        )

        result = list(self.client.cards_for_identifiers(['wgd23', 'rjg21']))
        self.assertListEqual(result, TestGetCardsByIds.mocked_cards)

        self.assertEqual(initial_post.call_count, 1)
        self.assertEqual(page_two_post.call_count, 1)
        self.assertEqual(page_three_post.call_count, 1)

        # check that the identifiers were sent in the request
        self.assertEqual(initial_post.last_request.json(), {'identifiers': ['wgd23', 'rjg21']})
        # no body for followup requests
        self.assertIsNone(page_two_post.last_request.text)
        self.assertIsNone(page_three_post.last_request.text)
