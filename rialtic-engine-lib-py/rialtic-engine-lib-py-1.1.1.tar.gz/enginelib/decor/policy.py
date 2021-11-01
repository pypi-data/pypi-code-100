import os
from copy import copy
from string import Formatter
from typing import List, Optional, Dict, Any

from dataUtils.DBClient import DBClient
from enginelib.claim_focus import ClaimFocus
from enginelib.claim_line_focus import ClaimLineFocus
from fhir.resources.claim import Claim
from schema.insight_engine_request import InsightEngineRequest
from schema.insight_engine_response import InsightEngineResponse, Insight, Defense, TranslatedMessage, MessageBundle

from enginelib.decor.traversal import TreeTraversal
from enginelib.decor.registry import Registry
from enginelib.decor.tree import Tree


class Policy:
    def __init__(self, request: InsightEngineRequest, historical_claims: List[Claim],
                 decision_tree: Tree, data: Optional[Dict[str, Any]] = None, engine_id: str = ''):
        self.cue = ClaimFocus(claim=request.claim, request=request)
        self.request = request
        self.historical_claims = [
            ClaimFocus(claim=claim, request=InsightEngineRequest.construct(claim=claim))
            for claim in historical_claims
        ]
        self.decision_tree = copy(decision_tree)
        self.data: Dict[str, Any] = data or dict()
        self.client = DBClient.GetDBClient(os.environ['APIKEY'])
        if engine_id:
            self.client.init_defenses(request.transaction_id or 'testing', engine_id=engine_id)

    def evaluate(self) -> InsightEngineResponse:
        """Evaluates the policy for each claim line in self.request.claim.

        Returns:
            a response with the response.insights containing the list of insights
        """
        self.decision_tree.assemble()
        response = InsightEngineResponse()
        response.insights = [
            self._assess(clue)
            for clue in self.cue.lines
        ]
        return response

    def _assess(self, clue: ClaimLineFocus) -> Insight:
        """Assess one claim line according to the decision tree of the policy.

        Args:
            clue: claim line to assess.

        Returns:
            an insight for the given claim line.
        """
        debug = os.getenv('DECOR_DEBUG', '')
        registry = Registry(cue=self.cue, clue=clue, ocs=self.historical_claims, data=copy(self.data))
        label = TreeTraversal(self.decision_tree, registry).execute()

        # Customize insight text with parameters in the registry
        EngineResult = self.decision_tree.ResultClass
        insight_type = EngineResult.insight_type[label]
        insight_text = EngineResult.insight_text[label]
        insight_text = self._format_insight_text(registry, insight_text, debug=debug)

        # DEBUGGING:
        if debug:
            self._log(f'      >>> Insight #{label}: {insight_type}; "{insight_text}"')
        if debug == 'testing':
            insight_text = label

        # Fetch defense data and create defense object
        excerpt, uuid = self.client.get_defense_by_node(label)
        defense = self.create_defense(text=excerpt, uuid=uuid)

        return Insight(
            id=self.request.claim.id,
            type=insight_type,
            description=insight_text,
            claim_line_sequence_num=clue.sequence,
            defense=defense
        )

    @staticmethod
    def _format_insight_text(registry: Registry, text: str, debug: str = '') -> str:
        # DEBUGGING
        if debug == 'parameters':
            print(end=f'The function _format_insight_text() was called with text {repr(text)}. ')
            print(f'The registry has the following parameters defined: {registry.computed_parameters_values}')

        keys = [i[1] for i in Formatter().parse(text) if i[1] is not None]
        data_dict = {
            key: str(registry[key]) if key in registry else '{' f'{key}' '}'
            for key in keys
        }
        return text.format(**data_dict)

    @staticmethod
    def create_defense(text: str = '', uuid: str = '') -> Defense:
        message = TranslatedMessage()
        message.lang = 'en'
        message.message = text

        script = MessageBundle()
        script.uuid = uuid
        script.messages = [message]

        defense = Defense()
        defense.script = script
        return defense

    @staticmethod
    def _log(msg_line: str):
        print(msg_line)
