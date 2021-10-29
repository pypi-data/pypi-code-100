from django.db.models import Q
from django.core.exceptions import PermissionDenied
from graphene_django.filter import DjangoFilterConnectionField
import graphene_django_optimizer as gql_optimizer

from django.utils.translation import gettext as _
from location.apps import LocationConfig
from core.schema import OrderedDjangoFilterConnectionField

# We do need all queries and mutations in the namespace here.
from .gql_queries import *  # lgtm [py/polluting-import]
from .gql_mutations import *  # lgtm [py/polluting-import]

class Query(graphene.ObjectType):
    payers = OrderedDjangoFilterConnectionField(
        PayerGQLType,
        parent_location=graphene.String(),
        parent_location_level=graphene.Int(),
        orderBy=graphene.List(of_type=graphene.String),
    )

    def resolve_payers(self, info, **kwargs):
        # if not info.context.user.has_perms(PayerConfig.gql_query_payers_perms):
        #     raise PermissionDenied(_("unauthorized"))
        filters = []
        # show_history = kwargs.get('show_history', False)
        # if not show_history and not kwargs.get('uuid', None):
        #     filters += filter_validity(**kwargs)
        parent_location = kwargs.get('parent_location')
        if parent_location is not None:
            parent_location_level = kwargs.get('parent_location_level')
            if parent_location_level is None:
                raise NotImplementedError("Missing parentLocationLevel argument when filtering on parentLocation")
            f = "uuid"
            for i in range(len(LocationConfig.location_types) - parent_location_level - 1):
                f = "parent__" + f
            payer_location = "location__" + f
            filters.append(Q(**{payer_location: parent_location}))
        return gql_optimizer.query(Payer.objects.filter(*filters).all(), info)
