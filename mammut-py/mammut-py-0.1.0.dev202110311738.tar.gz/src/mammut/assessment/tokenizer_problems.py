from mammut.assessment.problem import Problem
from mammut.curriculum.models.sentencepiece import SentencepieceBaseModel
from typing import List, Tuple, Dict


class SpecialTokenProblemMFT(Problem):
    """This class evaluates the encoding produced by a trained
    tokenizer.

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
        self._expected_tokens_dict = self.parameters["expected_tokens"]
        self._tokenized_output: str = ""

    def solve(self, model: SentencepieceBaseModel, **kwargs) -> bool:
        self._retries_count += 1
        subword_tokenizer = model.sp_preprocessor
        self._tokenized_output = subword_tokenizer.encode(
            self._input, out_type=str
        )
        for (
            expected_token,
            expected_occurences,
        ) in self._expected_tokens_dict.items():
            if (
                not self._tokenized_output.count(expected_token)
                == expected_occurences
            ):
                """
                    If count does not match, short circuit and return false.
                """
                return False

        return True

    def get_result_info(self) -> Dict:
        info = {
            "Tokenization Result": ", ".join(self._tokenized_output),
            "Expected tokens": self._expected_tokens_dict,
        }
        return info
