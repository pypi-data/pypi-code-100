from sentry_sdk._types import MYPY
from sentry_sdk.hub import Hub
from sentry_sdk.integrations import Integration
from sentry_sdk.scope import add_global_event_processor

import posthog
from posthoganalytics.request import DEFAULT_HOST
from posthoganalytics.sentry import POSTHOG_ID_TAG

if MYPY:
    from typing import Any, Dict, Optional

    from sentry_sdk._types import Event, Hint


class PostHogIntegration(Integration):
    identifier = "posthog-python"
    organization = None  # The Sentry organization, used to send a direct link from PostHog to Sentry
    project_id = None  # The Sentry project id, used to send a direct link from PostHog to Sentry
    prefix = "https://sentry.io/organizations/"  # Url of a self-hosted sentry instance (default: https://sentry.io/organizations/)

    @staticmethod
    def setup_once():
        @add_global_event_processor
        def processor(event, hint):
            # type: (Event, Optional[Hint]) -> Optional[Event]
            if Hub.current.get_integration(PostHogIntegration) is not None:
                if event.get("level") != "error":
                    return event

                if event.get("tags", {}).get(POSTHOG_ID_TAG):
                    posthog_distinct_id = event["tags"][POSTHOG_ID_TAG]
                    event["tags"]["PostHog URL"] = f"{posthog.host or DEFAULT_HOST}/person/{posthog_distinct_id}"

                    properties = {
                        "$sentry_event_id": event["event_id"],
                        "$sentry_exception": event["exception"],
                    }

                    if PostHogIntegration.organization and PostHogIntegration.project_id:
                        properties[
                            "$sentry_url"
                        ] = f"{PostHogIntegration.prefix}{PostHogIntegration.organization}/issues/?project={PostHogIntegration.project_id}&query={event['event_id']}"

                    posthog.capture(posthog_distinct_id, "$exception", properties)

            return event
