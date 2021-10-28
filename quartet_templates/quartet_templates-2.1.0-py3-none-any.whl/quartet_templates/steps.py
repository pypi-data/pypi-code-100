# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.

import sys
import random
from uuid import uuid4
from time import time
from datetime import datetime

from jinja2.environment import Environment
from quartet_templates.models import Template
from quartet_capture.rules import Step, RuleContext
from quartet_capture.models import Task
from quartet_output.steps import ContextKeys


class TemplateStep(Step):
    """
    Will load a template based on the step parameter "Template Name" and
    render it using a combination of rule data, context variables and
    the template variables.
    """

    def execute(self, data, rule_context: RuleContext):
        self.info('Looking for Step Parameter with name "Template Name"...')
        template_name = self.get_parameter(
            'Template Name',
            raise_exception=True
        )
        context_key = self.get_parameter("Context Key")
        self.info("Template Name parameter value found: %s.  "
                  "Looking up Template...", template_name)
        template = Template.objects.get(name=template_name)
        self.info("Found template...rendering...")
        environment = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=self.get_boolean_parameter('Auto Escape', True)
        )
        ret = template.render({'data': data, 'rule_context': rule_context,
                               'step_parameters': self.parameters,
                               'task_parameters': self.get_task_parameters(
                                   rule_context
                               ),
                               'epoch': time(),
                               'random': random.randint(1, sys.maxsize),
                               'UUID': str(uuid4()),
                               'datetime': datetime.isoformat(datetime.now())
                               }, environment=environment)
        self.info("Template response %s:", ret)
        if context_key:
            self.info("Placing rendered content into context key %s.",
                      context_key)
            rule_context.context[context_key] = ret
        else:
            self.info("Returning rendered content to the rule.")
            data = ret
        return data

    @property
    def declared_parameters(self):
        return {
            "Template Name": "The name of the template to load and render.",
            "Context Key": "The context key to place the output into.  If "
                           "none is specified, the output will be returned to "
                           "the rule in place of the inbound data.",
            "Auto Escape": "Whether or not the jinja2 template should be "
                           "auto escaped.  Default is True, set to False if "
                           "you are embedding XML within XML, etc."
        }

    def on_failure(self):
        pass


class ChangeTemplatesStep(Step):
    """
    Looks for aggregation, object and transaction events on the context using
    the context keys in quartet_output and changes the default template for
    each event.
    """

    def execute(self, data, rule_context: RuleContext):
        oe_template = self.get_parameter('Object Event Template')
        ae_template = self.get_parameter('Aggregation Event Template')
        self.chagne_object_event_template(rule_context, oe_template)
        self.change_aggregation_event_template(rule_context, ae_template)
        return data

    def chagne_object_event_template(self, rule_context: RuleContext,
                                     template_name:str):
        """
        Iterates through any object events in the OBJECT_EVENTS_KEY value
        from quartet_output context keys and changes each of the EPCPyYes
        template events' template to the one defined in step parameter as
        the Object Event Template
        :param rule_context: The rule context.
        :return: None
        """
        if template_name:
            object_events = rule_context.context.get(
                ContextKeys.OBJECT_EVENTS_KEY.value
            )
            if object_events:
                self.info('Changing the object events templates to %s',
                          template_name)
                self.change_templates(object_events, template_name)

    def change_aggregation_event_template(self, rule_context: RuleContext,
                                          template_name: str):
        """
        Iterates through any object events in the OBJECT_EVENTS_KEY value
        from quartet_output context keys and changes each of the EPCPyYes
        template events' template to the one defined in step parameter as
        the Object Event Template
        :param rule_context: The rule context.
        :return: None
        """
        if template_name:
            aggregation_events = rule_context.context.get(
                ContextKeys.AGGREGATION_EVENTS_KEY.value
            )
            if aggregation_events:
                self.info('Changing the aggregation events template to %s',
                          template_name)
                self.change_templates(aggregation_events, template_name)

    def change_transaction_event_template(self, rule_context: RuleContext):
        raise NotImplementedError(
            'This function has not yet been implemented.')

    def change_templates(self, events: list, template_name: str):
        try:
            template = Template.objects.get(name=template_name)
            for event in events:
                event.template = template.content
        except Template.DoesNotExist:
            self.error('Could not find a template with the name %s. '
                       'Make sure this is configured as a template.',
                       template_name)
            raise

    @property
    def declared_parameters(self):
        return {
            'Object Event Template': 'The name of the QU4RTET template to use for '
                                     'object events.',
            'Aggregation Event Template': 'The name of the QU4RTET template to use ' \
                                          'for aggregation events.',
            'Transaction Event Template': 'The transaction event template name.'
        }

    def on_failure(self):
        pass
