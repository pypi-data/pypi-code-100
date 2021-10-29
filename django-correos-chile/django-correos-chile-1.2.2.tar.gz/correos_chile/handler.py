# -*- coding: utf-8 -*-
import logging
from weasyprint import HTML
from zeep import Client, xsd
from zeep.helpers import serialize_object
from django.http import HttpResponse
from django.template.loader import render_to_string
from correos_chile.settings import api_settings

logger = logging.getLogger(__name__)


class CorreosHandler:
    """
        Handler to send shipping payload to Correos Chile.
    """

    def __init__(self, wsdl_url=api_settings.CORREOS_CHILE['EXECUTE_WSDL'],
                 user=api_settings.CORREOS_CHILE['USER'],
                 password=api_settings.CORREOS_CHILE['PASSWORD']):

        self.wsdl_url = wsdl_url
        self.user = user
        self.password = password

    def _headers(self):
        raise NotImplementedError(
            '_headers is not a method implemented for CorreosHandler')

    def get_shipping_label(self, instance, response_data):
        """
            This method generate a shipping label in pdf using the
            structure of Correos Chile.

            Arguments:
                instance: an instance object
                response_data: use the response of create_shipping()
        """
        html_string = render_to_string(
            'correos_chile/correos_slip.html', {
                'instance': instance,
                'raw_data': response_data
            }
        )
        pdf_rendered = HTML(string=html_string, base_url=api_settings.SENDER['DOMAIN']).write_pdf()
        response = HttpResponse(pdf_rendered, content_type='application/pdf;')
        response['Content-Disposition'] = f'filename=Etiqueta_Pedido_{instance.reference}.pdf'
        return response

    def get_default_payload(self, instance):
        """
            This method generates by default all the necessary data with
            an appropriate structure for Correos Chile courier.

            Returns default payload or AttributeError Exception.
        """
        payload = {
            'reference': instance.reference,
            'recipient_name': instance.customer.full_name,
            'recipient_address': f'{instance.address.street} {instance.address.number}',
            'recipient_postal_code': instance.commune.code,
            'recipient_commune': instance.commune.name,
            'recipient_rut': instance.customer.rut,
            'recipient_contact': instance.customer.full_name,
            'recipient_phone': instance.customer.phone
        }

        logger.debug(payload)
        return payload

    def create_shipping(self, data):
        """
            This method generate a Correos Chile shipping.
            If the get_default_payload method returns data, send it here,
            otherwise, generate your own payload.
        """
        logger.debug(data)

        client = Client(self.wsdl_url)
        client.set_ns_prefix('tns', 'http://tempuri.org/')

        type_data = client.get_type('tns:AdmisionTO')
        template = type_data(
            ExtensionData=xsd.SkipValue,
            CodigoAdmision=api_settings.SENDER['ADMISSION'],
            ClienteRemitente=api_settings.SENDER['CLIENT'],
            CentroRemitente=xsd.SkipValue,
            NombreRemitente=api_settings.SENDER['NAME'],
            DireccionRemitente=api_settings.SENDER['ADDRESS'],
            PaisRemitente=api_settings.SENDER['COUNTRY'],
            CodigoPostalRemitente=xsd.SkipValue,
            ComunaRemitente=api_settings.SENDER['CITY'],
            RutRemitente=api_settings.SENDER['RUT'],
            PersonaContactoRemitente=api_settings.SENDER['CONTACT_NAME'],
            TelefonoContactoRemitente=api_settings.SENDER['CONTACT_PHONE'],
            ClienteDestinatario=xsd.SkipValue,
            CentroDestinatario=xsd.SkipValue,
            NombreDestinatario=data['recipient_name'],
            DireccionDestinatario=data['recipient_address'],
            PaisDestinatario=api_settings.SENDER['COUNTRY'],
            CodigoPostalDestinatario=data['recipient_postal_code'],
            ComunaDestinatario=data['recipient_commune'],
            RutDestinatario=data['recipient_rut'],
            PersonaContactoDestinatario=data['recipient_contact'],
            TelefonoContactoDestinatario=data['recipient_phone'],
            CodigoServicio=api_settings.CORREOS_CHILE['COD_SERVICIO'],
            NumeroTotalPiezas='1',
            Kilos='1',
            Volumen='0',
            NumeroReferencia=f"{api_settings.CORREOS_CHILE['COD_REF']} - {data['reference']}",
            ImporteReembolso='0',
            ImporteValorDeclarado='0',
            TipoPortes=api_settings.CORREOS_CHILE['TYPE_POR'],
            Observaciones=xsd.SkipValue,
            Observaciones2=xsd.SkipValue,
            EmailDestino=xsd.SkipValue,
            TipoMercancia=xsd.SkipValue,
            DevolucionConforme=api_settings.CORREOS_CHILE['DEV_CON'],
            NumeroDocumentos='0',
            PagoSeguro=xsd.SkipValue
        )

        try:
            zeep_response = client.service.admitirEnvio(
                usuario=self.user,
                contrasena=self.password,
                admisionTo=template
            )
            response = dict(serialize_object(zeep_response))
            response.update({'tracking_number': response['NumeroEnvio']})

            logger.debug(response)
            return response
        except Exception as error:
            logger.error(error)
            return False

    def get_tracking(self, identifier):
        """
            This method obtain a detail a shipping of Correos Chile.
        """
        raise NotImplementedError(
            'get_tracking is not a method implemented for CorreosHandler')

    def get_events(self, raw_data):
        """
            This method obtain array events.
            structure:
            {
                'expedicion': '990077324935',
                'referencia': 'CLV-10000001',
                'estado_2': 'ENVIO ENTREGADO',
                'fechaEvento': '12/12/2021',
                'fechaCarga': '12/12/2021',
                'estadoBase': 'Envio en reparto',
                'ciudad': 'Santiago'
            }
            return [
                {
                    'city': 'Santiago',
                    'state':, 'description': 'ENVIO ENTREGADO',
                    'date': '12/12/2021'
                }
            ]
        """

        status = raw_data.get('estado_2')

        events = [{
            'city': raw_data.get('ciudad'),
            'state': '',
            'description': status,
            'date': raw_data.get('fechaEvento'),
        }]

        return events

    def get_status(self, raw_data):
        """
            This method returns the status of the order and "is_delivered".
            structure:
            {
                'expedicion': '990077324935',
                'referencia': 'CLV-10000001',
                'estado_2': 'ENVIO ENTREGADO',
                'fechaEvento': '12/12/2021',
                'fechaCarga': '12/12/2021',
                'estadoBase': 'Envio en reparto',
                'ciudad': 'Santiago'
            }

            response: ('ENVIO ENTREGADO', True)
        """

        status = raw_data.get('estado_2')
        is_delivered = False

        if status in ['ENVIO ENTREGADO', 'ENVÍO ENTREGADO']:
            is_delivered = True

        return status, is_delivered
