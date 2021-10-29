# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``views`` module defines ``View`` objects for converting web requests
into rendered responses.

.. autosummary::
   :nosignatures:

   broker_web.apps.objects.views.ObjectsJsonView
   broker_web.apps.objects.views.RecentAlertsJsonView
   broker_web.apps.objects.views.ObjectSummaryView
   broker_web.apps.objects.views.RecentObjectsView
"""

import os

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from google.cloud import bigquery

from .forms import FilterObjectsForm
from ..utils import paginate_to_json
from ..utils.templatetags.utility_tags import jd_to_readable_date

if 'BUILD_IN_RTD' not in os.environ:
    CLIENT = bigquery.Client()


###############################################################################
# JSON views
###############################################################################

class RecentObjectsJsonView(View):
    """View for serving recently observed objects as a paginated JSON response"""

    @staticmethod
    def fetch_objects(limit=10_000):
        """Returns a list of objects with recently issued alerts as a list of dicts

        Args:
            limit (int): Maximum number of alerts to return

        Return:
            A list of dictionaries representing
        """

        # Select the most recent alert for each object
        query = CLIENT.query(f"""
            SELECT 
                DISTINCT objectId as object_id, 
                publisher,
                CAST(candidate.candid AS STRING) recent_alert_id, 
                candidate.jd as pub_time,
                ARRAY_LENGTH( prv_candidates ) as num_alerts,
                ROUND(candidate.ra, 2) as ra, 
                ROUND(candidate.dec, 2) as dec
            FROM `{settings.ZTF_ALERTS_TABLE_NAME}`
            ORDER BY pub_time DESC
            LIMIT {limit}
           """)

        output = []
        for row in query.result():
            row = dict(row)
            row['pub_time'] = jd_to_readable_date(row['pub_time'])
            output.append(row)

        return output

    def get(self, request):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing JsonResponse
        """

        # Get all available messages
        objects = self.fetch_objects()
        return paginate_to_json(request, objects)


class RecentObjectAlertsJsonView(View):
    """JSON rendering of recent alerts for a given object"""

    @staticmethod
    def fetch_object_alerts(object_id, limit=50):
        """Return a list of all alerts corresponding to an object Id

        Args:
            object_id (str): Object identifier
            limit     (int): Maximum number of alerts to return

        Returns:
            A list of dictionaries
        """

        # Select all alerts for the given object
        query = CLIENT.query(f"""
            SELECT 
                 publisher,
                 candidate.jd as pub_time,
                 CAST(candidate.candid AS STRING) as alert_id,
                 CASE candidate.fid WHEN 1 THEN 'g' WHEN 2 THEN 'R' WHEN 3 THEN 'i' END as filter,
                 ROUND(candidate.magpsf, 2) as magnitude
            FROM `{settings.ZTF_ALERTS_TABLE_NAME}`
            WHERE objectId="{object_id}"
            LIMIT {limit}
        """)

        out_data = []
        for row in query.result():
            row_dict = dict(row)
            row_dict['jd'] = row_dict['pub_time']
            row_dict['pub_time'] = jd_to_readable_date(row_dict['pub_time'])
            out_data.append(row_dict)

        return out_data

    def get(self, request, *args, **kwargs):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing JsonResponse
        """

        # Get all available messages
        alerts = self.fetch_object_alerts(kwargs['pk'])
        return paginate_to_json(request, alerts)


class Salt2FitsJsonView(View):
    """View for serving recent Salt2 fit results as a paginated JSON response"""

    @staticmethod
    def fetch_salt2_fits(object_id=None, limit=1000):
        """Return a list of recent Salt2 fits for a given astronomical object

        Args:
            object_id (str): Object identifier
            limit     (int): Maximum number of fits to return

        Returns:
            A list of dictionaries
        """

        condition = 'success=1'
        if object_id:  # Select all alerts for the given object
            condition += f' AND objectId="{object_id}"'

        query = CLIENT.query(f"""
            SELECT
                objectId as object_id,
                CAST(candId AS STRING) as alert_id,  
                ROUND(chisq, 2) as chisq, 
                ndof,
                ROUND(z, 4) as z, 
                ROUND(z_err, 6) as z_err,
                ROUND(t0, 2) as t0, 
                ROUND(t0_err, 4) as t0_err,
                ROUND(x0, 6) as x0, 
                ROUND(x0_err, 8) as x0_err,      
                ROUND(x1, 2) as x1, 
                ROUND(x1_err, 4) as x1_err,     
                ROUND(c, 2) as c, 
                ROUND(c_err, 4) as c_err,
            FROM  `{settings.ZTF_SALT2_TABLE_NAME}`
            WHERE {condition}
            LIMIT {limit}
        """)

        return [dict(row) for row in query.result()]

    def get(self, request, *args, **kwargs):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing JsonResponse
        """

        json_data = self.fetch_salt2_fits(object_id=kwargs.get('pk', None))
        return paginate_to_json(request, json_data)


###############################################################################
# Views for individual web pages
###############################################################################

class RecentObjectsView(View):
    """View for displaying a summary table of objects with recent alerts"""

    template = 'objects/recent_objects.html'

    def get(self, request):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing HTTPResponse
        """

        context = {'form': FilterObjectsForm()}
        return render(request, self.template, context)

    def post(self, request):
        """Fill in the page's form with values from the POST request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing HTTPResponse
        """

        form = FilterObjectsForm(request.POST)
        return render(request, self.template, {'form': form})


class ObjectSummaryView(View):
    """View for displaying a table of all recent objects matching a query"""

    template = 'objects/object_summary.html'

    def get(self, request, *args, **kwargs):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing JsonResponse
        """

        return render(request, self.template, context={
            'object_id': kwargs['pk'],
            'salt2_image_bucket': settings.ZTF_SALT2_IMAGE_BUCKET})


class Salt2FitView(View):
    """View for displaying a table of salt2 fits to recently observed objects"""

    template = 'objects/salt2_fits.html'

    def get(self, request, *args, **kwargs):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing JsonResponse
        """

        return render(request, self.template)
