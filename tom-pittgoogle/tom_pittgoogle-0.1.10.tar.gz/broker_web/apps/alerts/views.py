# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``views`` module defines ``View`` objects for converting web requests
into rendered responses.

.. autosummary::
   :nosignatures:

   broker_web.apps.alerts.views.AlertsJsonView
   broker_web.apps.alerts.views.AlertSummaryView
   broker_web.apps.alerts.views.RecentAlertsView
"""

import os

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from google.api_core.exceptions import BadRequest
from google.cloud import bigquery

from .forms import FilterAlertsForm
from ..utils import paginate_to_json
from ..utils.templatetags.utility_tags import jd_to_readable_date

NUM_ALERTS = 10_000

if 'BUILD_IN_RTD' not in os.environ:
    CLIENT = bigquery.Client()


class AlertsJsonView(View):
    """Serves recent alerts as a paginated JSON response"""

    @staticmethod
    def fetch_alerts_as_dicts(request, num_alerts=NUM_ALERTS):
        """Returns a list of recent alerts messages as dicts

        Args:
            request (HttpRequest): Incoming HTTP request
            num_alerts      (int): Maximum number of alerts to return

        Return:
            A list of dictionaries representing
        """

        # Select top most recent alerts
        query = CLIENT.query(f"""
            SELECT
                publisher, 
                CAST(candidate.candid AS STRING) as alert_id,
                CASE candidate.fid WHEN 1 THEN 'g' WHEN 2 THEN 'R' WHEN 3 THEN 'i' END as filter,
                ROUND(candidate.magpsf, 2) as magnitude,
                objectId as object_id, 
                candidate.jd as pub_time, 
                ROUND(candidate.ra, 2) as ra, 
                ROUND(candidate.dec, 2) as dec 
            FROM `{settings.ZTF_ALERTS_TABLE_NAME}` 
            ORDER BY pub_time DESC
            LIMIT {num_alerts}
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

        alerts = self.fetch_alerts_as_dicts(request)
        return paginate_to_json(request, alerts)


class RecentAlertsView(View):
    """Provides a summary table of recently ingested alerts"""

    template = 'alerts/recent-alerts.html'

    def get(self, request):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing HTTPResponse
        """

        context = {'form': FilterAlertsForm()}
        return render(request, self.template, context)

    def post(self, request):  # Todo: Add filtering from form and update tests
        """Fill in the page's form with values from the POST request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing HTTPResponse
        """

        form = FilterAlertsForm(request.POST)
        return render(request, self.template, {'form': form})


class AlertSummaryView(View):
    """Displays information about a single alert"""

    template = 'alerts/alert_summary.html'

    @staticmethod
    def _get_ztf_alert_data(alert_id):
        """Retrieve alert data for a ZTF alert ID

        Args:
            alert_id (int): Id of the alert to retrieve data for

        Return:
            A dictionary of alert data if available else None
        """

        query = CLIENT.query(f"""
            SELECT 
                schemavsn, publisher, objectId, candid, candidate, 
                cutoutScience.stampData as cutout_science, 
                cutoutTemplate.stampData as cutout_template, 
                cutoutDifference.stampData as cutout_difference
            FROM `{settings.ZTF_ALERTS_TABLE_NAME}` 
            WHERE candidate.candid={alert_id}
        """)

        try:
            query_result = query.result()

        except BadRequest:  # Alert id was likely a string and thus invalid
            return None

        # Return first value from the iterable
        for row in query_result:
            out_data = dict()
            for k, v in row.items():
                if isinstance(v, dict):  # Support for nested dictionaries
                    out_data.update(v)

                else:
                    out_data[k] = v

            return out_data

    def get_alert_data_for_id(self, alert_id, survey):
        """Retrieve alert data for a given alert ID

        Args:
            alert_id (int): Id of the alert to retrieve data for
            survey   (str): Parent survey of the alert

        Return:
            A dictionary of alert data
        """

        if survey.lower() == 'ztf':
            return self._get_ztf_alert_data(alert_id)

        raise NotImplementedError(f'Database alert queries not implemented for survey {survey}')

    @staticmethod
    def get_value_added_data_for_id(alert_id, survey):
        """Retrieve value added data products for a given alert ID

        Args:
            alert_id (int): Id of the alert to retrieve data for
            survey   (str): Parent survey of the alert

        Return:
            A dictionary of value added data products
        """

        # Todo: This function can probably be broken into multiple
        # functions based on different data products. It depends
        # how the back / front end is designed
        return dict()

    def get(self, request, *args, **kwargs):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing JsonResponse
        """

        alert_id = kwargs['pk']
        survey = kwargs.get('survey', 'ztf')
        alert_data = self.get_alert_data_for_id(alert_id, survey)
        if alert_data is None:
            return render(request, 'alerts/error_404.html', {'alert_id': alert_id})

        context = {
            'alert_data': alert_data,
            'alert_id': alert_id,
            'survey': survey,
            'science_image': alert_data.pop('cutout_science'),
            'template_image': alert_data.pop('cutout_template'),
            'difference_image': alert_data.pop('cutout_difference')
        }

        return render(request, self.template, context)
