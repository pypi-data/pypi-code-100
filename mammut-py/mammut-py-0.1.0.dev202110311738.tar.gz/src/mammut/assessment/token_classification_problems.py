from mammut.assessment.problem import Problem
from mammut.curriculum.models.hugging_face.roberta import (
    HuggingFaceRobertaTokenClassificationModel,
)
from typing import Dict
import torch


class RobertaTokenClassificationProblemMFT(Problem):
    """This class evaluates the encoding produced by a token classification
    model.

    Test the minimal functionality: expected token(s) is(are) found in the
    encoded output.
    """

    def __init__(
        self,
        course_id: str,
        assessment_id: str,
        schedule: str,
        problem_id: str,
        problem_type: str,
        parameters: str,
        language_competence: str,
        weight: str,
        retry: str,
        observations: str,
    ):
        """
        Args:
            course_id(str): id of the course to which this problem belongs.
            assessment_id(str): id of the assessment that bundles this problem.
            schedule(str): lesson schedule to execute this problem.
            problem_id(str): id for this problem.
            problem_type(str): problem type enumeration string.
            parameters (str): JSON string parameters for this problem.
            language_competence(str): language competence enumeration value for this problem.
            weight(str): float string value for the weight of this particular problem
                in the overall course score.
            observations(str): observations string. Only descriptive.
        """
        Problem.__init__(
            self,
            course_id,
            assessment_id,
            schedule,
            problem_id,
            problem_type,
            parameters,
            language_competence,
            weight,
            retry,
            observations,
        )
        self._input: str = self.parameters["input"]
        self._expected_classification_dict = self.parameters[
            "expected_classification"
        ]
        self._classification_output: str = ""

    def _token_classification(self, examples, model):

        tokens = model._tokenizer.tokenize(
            model._tokenizer.decode(model._tokenizer.encode(examples))
        )
        inputs = model._tokenizer.encode(
            examples, return_tensors="pt", padding=True, truncation=False
        )
        outputs = model(inputs).logits
        predictions = torch.argmax(outputs, dim=2)
        prediction = predictions[0].tolist()
        classification = [
            (token, model.labels[pred])
            for token, pred in zip(tokens, prediction)
        ]
        results = dict((y, x) for x, y in classification)
        return results

    def solve(
        self, model: HuggingFaceRobertaTokenClassificationModel, **kwargs
    ) -> bool:
        self._retries_count += 1
        self._classification_output = self._token_classification(
            self._input, model
        )
        if self._classification_output == self._expected_classification_dict:
            return True
        else:
            return False

    def get_result_info(self) -> Dict:
        info = {
            "Tokens classification result": ", ".join(
                self._classification_output
            ),
            "Expected classification": self._expected_classification_dict,
        }
        return info
