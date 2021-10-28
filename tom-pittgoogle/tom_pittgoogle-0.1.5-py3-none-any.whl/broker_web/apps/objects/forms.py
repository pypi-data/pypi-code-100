# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``forms`` module defines views forms for data entry and query
construction.

.. autosummary::
   :nosignatures:

   broker_web.apps.objects.forms.FilterObjectsForm
"""

from django import forms

topics = (
    'ztf_all',
    '91bg',
    'sne Ia',
    'CV'
)


# Todo: This form is almost identical to the FilterAlertsForm from the
# alerts app. I expect moving forward the two will diverge, but if that
# is not the case, consider making things more dry
class FilterObjectsForm(forms.Form):
    """Form for filtering a table of alerted objects

    Fields:
        time_range (``DurationField``)
        min_ra (``FloatField``)
        max_ra (``FloatField``)
        min_dec (``FloatField``)
        max_dec (``FloatField``)
    """

    time_range = forms.DurationField(required=False, label='Publication time')
    min_ra = forms.FloatField(
        required=False,
        label='Min RA',
        widget=forms.TextInput()
    )

    max_ra = forms.FloatField(required=False, label='Max RA', widget=forms.TextInput())
    min_dec = forms.FloatField(required=False, label='Min Dec', widget=forms.TextInput())
    max_dec = forms.FloatField(required=False, label='Max Dec', widget=forms.TextInput())
