# -*- coding: utf-8 -*-
import logging

from spread.connector import Connector, ConnectorException
from spread.settings import api_settings

logger = logging.getLogger(__name__)


class SpreadHandler:
    """
        Handler to send shipping payload to Spread
    """

    def __init__(self, base_url=api_settings.SPREAD['BASE_URL'],
                 id=api_settings.SPREAD['ID'],
                 secret=api_settings.SPREAD['SECRET'],
                 verify=True):

        self.base_url = base_url
        self.id = id
        self.secret = secret
        self.verify = verify
        self.connector = Connector(self._headers(), verify_ssl=self.verify)

    def _headers(self):
        """
            Here define the headers for all connections with Spread.
        """
        return {
            'client_id': self.id,
            'client_secret': self.secret,
            'Content-Type': 'application/json',
        }

    def get_shipping_label(self):
        raise NotImplementedError(
            'get_shipping_label is not a method implemented for SpreadHandler')

    def get_default_payload(self, instance):
        """
            This method generates by default all the necessary data with
            an appropriate structure for Spread courier.
        """

        payload = {
            'guide': instance.purchase_number,
            'name_client': instance.customer.full_name,
            'email': '',
            'phone': instance.customer.phone,
            'street': instance.address.street,
            'number': instance.address.number,
            'commune': instance.commune.name,
            'dpto_bloque': instance.address.unit,
            'fecha_retiro': ''
        }

        logger.debug(payload)
        return payload

    def create_shipping(self, data):
        """
            This method generate a Spread shipping.
            If the get_default_payload method returns data, send it here,
            otherwise, generate your own payload.
        """

        url = f'{self.base_url}pedidos'
        logger.debug(data)
        try:
            response = self.connector.post(url, data)
            if response.get('ok') == 'true':
                response.update({'tracking_url': response.get('url_tracking')})
                return response
            else:
                raise ConnectorException(response['message'], 'Error requesting create shipping', response.code)

        except ConnectorException as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error

    def get_tracking(self, identifier):
        raise NotImplementedError(
            'get_tracking is not a method implemented for SpreadHandler')

    def get_events(self, raw_data):
        """
            This method obtain array events.
            structure:
            {
                'tracking_number': 999999,
                'status': 'entregado',
                'events': [{
                    'city': 'Santiago',
                    'state': 'RM',
                    'description': 'Llego al almacén',
                    'date': '12/12/2021'
                }]
            }
            return [{
                'city': 'Santiago',
                'state': 'RM',
                'description': 'Llego al almacén',
                'date': '12/12/2021'
            }]
        """
        return raw_data.get('events')

    def get_status(self, raw_data):
        """
            This method returns the status of the order and "is_delivered".
            structure:
            {
                'tracking_number': 999999,
                'status': 'entregado',
                'events': [{
                    'city': 'Santiago',
                    'state': 'RM',
                    'description': 'Llego al almacén',
                    'date': '12/12/2021'
                }]
            }

            status : [Ingresado, Recepcionado correctamente, No recepcionado, asignado a ruta,
                      entregado, No entregado, Devuelto a logística Inversa]
            response: ('entregado', True)
        """

        status = raw_data.get('status')
        is_delivered = False

        if status.capitalize() == 'Entregado':
            is_delivered = True

        return status, is_delivered
