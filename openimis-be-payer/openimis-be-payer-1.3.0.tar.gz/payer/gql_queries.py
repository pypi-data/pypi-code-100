import graphene
from graphene_django import DjangoObjectType
from .models import Payer
from location.schema import LocationGQLType
from core import prefix_filterset, filter_validity, ExtendedConnection

class PayerGQLType(DjangoObjectType):
    class Meta:
        model = Payer
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "uuid": ["exact"],
            "name": ["exact", "icontains"],
        }
        connection_class = ExtendedConnection
