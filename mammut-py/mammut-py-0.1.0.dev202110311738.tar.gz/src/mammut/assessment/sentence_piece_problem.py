import string
import itertools
import pandas as pd
from mammut.assessment.problem import Problem
from mammut.curriculum.models.sentencepiece import SentencepieceBaseModel
from typing import List, Tuple, Dict
import re


class SentencepieceProblemMFT(Problem):
    """Concrete class to evaluate Google sentencepiece
    trained models.

    Test a minimal functionality expected in the
    discovered vocabulary.

    Note: receives string values from storage manager
        retrieved dataset.
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
        """
            Template base tags specified for this problem.
            For example:
                {root} {flex1} {flex2}
        """
        self._template_base: str = ""
        """
            _filled_template attribute contains the lists of values for the 
            template tags.
        """
        self._filled_template: List[List[str]] = []
        """
            _rendered_segmented_words contains a list of the expected segmentation
            strings given the template arguments for this test. 
            
            For example:
                [('est', 'uvi', 'era'),
                 ('est', 'uvi', 'ese'),
                 ('est', 'uvi', 'eras'),
                 ('est', 'uvi', 'eses'),
                 ('est', 'uvi', 'era'),
                 ('est', 'uvi', 'ese'),
                 ('est', 'uvi', 'eramos'),
                 ('est', 'uvi', 'esemos'),
                 ('est', 'uvi', 'eran'),
                 ('est', 'uvi', 'esen')]
        """
        self._rendered_segmented_words: List[Tuple[str]] = []
        """
            _rendered_words contains the list of rendered words for the template
        """
        self._rendered_words: List[str] = []
        self._parse_parameters()
        self._render_segmented_words()
        self._render_words()

    def _parse_parameters(self):
        template_base_rgx = re.compile("\{(.*?)\}+")
        self._template_base = self.parameters["template_base"]
        """
            Take the words from the string tags.
            Joins them by comma, converts to a list by splitting.
            {root} {flex} -> ['root', 'flex']
        """
        template_base_words_list = ",".join(
            template_base_rgx.findall(self.parameters["template_base"])
        ).split(",")
        for word in template_base_words_list:
            self._filled_template.append(self.parameters[word])

    def _render_segmented_words(self):
        """This method computes by segments the rendered words
                from the 'render_words' method.

            Example:
                input: [['invent', 'rebaj', 'plasm', 'labr', 'lav',
                    'habit', 'habl'], ['o', 'as', 'a', 'amos', 'áis', 'an']]
                output: [('invent', 'o'), ('invent', 'as'), ('invent', 'a'),
                    ('invent', 'amos'), ('invent', 'áis'), ('invent', 'an'),
                    ('rebaj', 'o'), ('rebaj', 'as'), ('rebaj', 'a'), ('rebaj', 'amos'),
                    ('rebaj', 'áis'), ('rebaj', 'an'), ('plasm', 'o'), ('plasm', 'as'),
                    ('plasm', 'a'), ('plasm', 'amos'), ('plasm', 'áis'), ('plasm', 'an'),
                    ('labr', 'o'), ('labr', 'as'), ('labr', 'a'), ('labr', 'amos'),
                    ('labr', 'áis'), ('labr', 'an'), ('lav', 'o'), ('lav', 'as'),
                    ('lav', 'a'), ('lav', 'amos'), ('lav', 'áis'), ('lav', 'an'),
                    ('habit', 'o'), ('habit', 'as'), ('habit', 'a'), ('habit', 'amos'),
                    ('habit', 'áis'), ('habit', 'an'), ('habl', 'o'), ('habl', 'as'),
                    ('habl', 'a'), ('habl', 'amos'), ('habl', 'áis'), ('habl', 'an')]

            Return:
                Returns a list of segmented words.
        """
        words = [m for m in itertools.product(*self._filled_template)]
        render_seg_words = [word for word in words]
        self._rendered_segmented_words = render_seg_words

    def _render_words(self):
        """This method a list of the words that can be built with the template.

           Example:
               input: [['invent', 'rebaj', 'plasm', 'labr', 'lav',
                   'habit', 'habl'], ['o', 'as', 'a', 'amos', 'áis', 'an']]
               output: ['invento', 'inventas', 'inventa', 'inventamos',
                   'inventáis', 'inventan', 'rebajo', 'rebajas', 'rebaja',
                   'rebajamos', 'rebajáis', 'rebajan', 'plasmo', 'plasmas',
                   'plasma', 'plasmamos', 'plasmáis', 'plasman', 'labro',
                   'labras', 'labra', 'labramos', 'labráis', 'labran', 'lavo',
                   'lavas', 'lava', 'lavamos', 'laváis', 'lavan', 'habito',
                   'habitas', 'habita', 'habitamos', 'habitáis', 'habitan',
                   'hablo', 'hablas', 'habla', 'hablamos', 'habláis', 'hablan']

           Return:
               Returns a list of words built.
       """
        words = [m for m in itertools.product(*self._filled_template)]
        self._rendered_words = ["".join(word) for word in words]

    def _test_run(self, subword_tokenizer, whitespace: bool = False):
        """Runs a test to check that the segmentation built into
            a template is equal to the segmentation of the rendered
            word made by a subword_tokenizer.

            This method works with the 'template method' which defines
            separate morphemes of words, and the 'render_words method'
            which builds the words.

            The test consists of taking as an argument a morpheme tokenizer,
            that takes the separate morphemes of a word. Then the tokenizer
            is used to segment the rendered word and the result is compared
            with the word segmented by the template method.

            Args:
                subword_tokenizer: an object that represents a tokenization model.
                whitespace(bool): False by default. If True, at the
                    time of testing it ignores the white space produced
                    by SentencePiece's subword_tokenizer.
        """
        test_successful = list()
        test_failed = list()
        for num_test in range(len(self._rendered_segmented_words)):
            expected = [
                m for m in self._rendered_segmented_words[num_test] if m != ""
            ]
            if whitespace:
                predicted_whitespace = subword_tokenizer.encode(
                    self.words[num_test], out_type=str
                )
                predicted = [m.replace("▁", "") for m in predicted_whitespace]
            else:
                predicted = subword_tokenizer.encode(
                    self._rendered_words[num_test], out_type=str
                )
            if expected == predicted:
                test_successful.append(predicted)
            else:
                test_failed.append(predicted)
        """
            The test was successful if all the words were segmented as 
            expected.
        """
        return len(test_successful) == len(self._rendered_segmented_words)

    def solve(self, model: SentencepieceBaseModel, **kwargs) -> bool:
        self._retries_count += 1
        return self._test_run(
            model.sp_preprocessor, kwargs["whitespace_as_prefix"]
        )

    def get_result_info(self) -> Dict:
        info = {"Test info": "Nothing to show yet"}
        return info


class SentencepieceProblemINV(Problem):
    """Class purpose is to conduct 'Invariance Test' for vocabulary.

    Perturbation types offered by this class:
        -substitution.
        -punctuation marks.
        -capitalization.
        -uppercase.
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
        self._words = self.parameters["words"]
        self._substituted_words: List[Dict] = []
        """
            JSON parameters can specifiy substitutions
        """
        if "substitutions" in self.parameters:
            self._substitution_requested = True
            self._substitution(self.parameters["substitutions"])
        else:
            self._substitution_requested = False

    def _zip_lists(self, list1: list, list2: list):
        zipped_list = list()
        for i in range(len(list2)):
            zipped_list.append([list1[i], list2[i]])
        if list1[-1] != [""]:
            zipped_list.append(list1[-1])
        return zipped_list

    def _check_test(self, expected: list, predicted: list) -> bool:
        return len(expected) == len(predicted)

    def _check_test_punct(self, expected: list, predicted: list) -> bool:
        return len(expected) == len(predicted) - 1

    def _substitution(self, substitutions: dict) -> list:
        """This method takes as an argument a dictionary in which a key
        represents a letter or segment found in one or more of the words
        of the class "Perturb", and the value is a list of letters or
        segments that replace the corresponding key. It searches the words
        to be tested and replaces the letters according to the value of the
        dictionary.

        Args:
            substitutions(dict): dictionary in which each key represents
                a letter or segment found in one or more of the words of
                the class "Perturb".

        Example:
            input: {'a': ['a', 'o']}
            output: [{'niña': [['niñ'], ['a', 'o']]},
                {'lora': [['lor'], ['a', 'o']]},
                {'enfermera': [['enfermer'], ['a', 'o']]},
                {'dueña': [['dueñ'], ['a', 'o']]}]

        Returns:
            Returns a list of dictionaries.
        """
        # not working when a substitution is not in all words.
        ret_words = list()
        for s in substitutions.items():
            source = s[0]
            target = s[1]
            for w in self._words:
                constant = [[m] for m in w.split(source)]
                if constant[0] == "":
                    constant[0] = source
                substitutions = [target]
                ret_word = self._zip_lists(
                    constant, (substitutions * (len(constant) - 1))
                )
                ret_words.append({w: [j for i in ret_word for j in i]})
        self._substituted_words = ret_words
        return ret_words

    def _substitution_render_words(self) -> list:
        """This method renders the words as defined in the
        'substitution method'.

        Example:
            output: [{'niña': ['niña', 'niño']},
                {'lora': ['lora', 'loro']},
                {'enfermera': ['enfermera', 'enfermero']},
                {'dueña': ['dueña', 'dueño']}]

        Returns:
            Returns a list of words.
        """
        render_words = list()
        for word in self._substituted_words:
            w = list(word.values())[0]
            original = list(word.keys())[0]
            words = [m for m in itertools.product(*w)]
            render_word = ["".join(word) for word in words]
            render_words.append({original: render_word})
        return render_words

    def _test_substitution(self, subword_tokenizer) -> bool:
        """This method returns the results of the subword_tokenizer,
        for the words in which a substitution disturbance has been
        made through the 'substitution method'.

        Args:
            subword_tokenizer: an object that represents a tokenization model.

        Returns:
            Returns the results of the subword_tokenizer.
        """
        ret_words = self._substitution_render_words()
        if not self._substitution_requested:
            return True
        else:
            return self._test_run(
                ret_words, subword_tokenizer, self._check_test
            )

    def _punctuation_marks(self):
        """This method adds punctuation marks to the words rendered with
        the 'substitution_render_words method'.

        Example:
            output: [{'niña': ['niña?', 'niña!', 'niña,', 'niña.', 'niña;', 'niña:', 'niña-']},
                {'lora': ['lora?', 'lora!', 'lora,', 'lora.', 'lora;', 'lora:', 'lora-']},
                {'enfermera': ['enfermera?',
                'enfermera!',
                'enfermera,',
                'enfermera.',
                'enfermera;',
                'enfermera:',
                'enfermera-']},
                {'dueña': ['dueña?',
                'dueña!',
                'dueña,',
                'dueña.',
                'dueña;',
                'dueña:',
                'dueña-']}]

        Returns:
            Returns a list of words.
        """
        ret_words = list()
        marks = ["?", "!", ",", ".", ";", ":", "-"]
        for w in self._words:
            ret_words.append({w: [w + m for m in marks]})
        return ret_words

    def _test_punctuation_marks(self, subword_tokenizer):
        """This method returns the results of the subword_tokenizer,
        for the words in which punctuation_marks have been
        added through the 'punctuation_marks method'.

        Args:
            subword_tokenizer: an object that represents a tokenization model.

        Returns:
            Returns the results of the subword_tokenizer.
        """
        ret_words = self._punctuation_marks()
        return self._test_run(
            ret_words, subword_tokenizer, self._check_test_punct
        )

    def _uppercase(self):
        """This method changes words to uppercase.

        Example:
            output: [{'bailaba': ['BAILABA']}, {'tronaba':
            ['TRONABA']}, {'gastaba': ['GASTABA']}]

        Returns:
            Returns a list of words.
        """
        return [{w: [w.upper()]} for w in self._words]

    def _test_uppercase(self, subword_tokenizer):
        """This method returns the results of the subword_tokenizer,
        for the words that were changed to uppercase through the
        'uppercase method'.

        Args:
            subword_tokenizer: an object that represents a tokenization model.

        Returns:
            Returns the results of the subword_tokenizer.
        """
        ret_words = self._uppercase()
        return self._test_run(ret_words, subword_tokenizer, self._check_test)

    def _capitals(self):
        """This method capitalizes words.

        Example:
            output: [{'niña': ['Niña']},
                {'lora': ['Lora']},
                {'enfermera': ['Enfermera']},
                {'dueña': ['Dueña']}]

        Returns:
            Returns a list of words.
        """
        return [{w: [w.capitalize()]} for w in self.words]

    def _test_capitals(self, subword_tokenizer):
        """This method returns the results of the subword_tokenizer,
        for the words which were capitalize through the 'capitals
        method'.

        Args:
            subword_tokenizer: an object that represents a tokenization model.

        Returns:
            Returns the results of the subword_tokenizer.
        """
        ret_words = self.capitals()
        return self._test_run(ret_words, subword_tokenizer, self._check_test)

    def _test_run(self, ret_words: list, subword_tokenizer, check) -> bool:
        test_successful = list()
        test_failed = list()
        total_tested_cases: int = 0
        for w in ret_words:
            for k, v in w.items():
                for num_test in range(len(v)):
                    expected = subword_tokenizer.encode(k, out_type=str)
                    predicted = subword_tokenizer.encode(
                        v[num_test], out_type=str
                    )
                    total_tested_cases += 1
                    if check(expected, predicted):
                        test_successful.append(predicted)
                    else:
                        test_failed.append(predicted)
        return len(test_successful) == total_tested_cases

    def solve(self, model: SentencepieceBaseModel, **kwargs) -> bool:
        self._retries_count += 1
        substitution_solved = self._test_substitution(model.sp_preprocessor)
        uppercase_solver = self._test_uppercase(model.sp_preprocessor)
        capitals_solved = self._test_capitals(model.sp_preprocessor)
        punctuations_solved = self._test_punctuation_marks(
            model.sp_preprocessor
        )
        return (
            substitution_solved
            and uppercase_solver
            and capitals_solved
            and punctuations_solved
        )

    def get_result_info(self) -> Dict:
        info = {"Test info": "Nothing to show yet"}
        return info


def MFT_vocab_test(test_cases: list, subword_tokenizer):
    def _check_test(expected: list, predicted: list) -> bool:
        return expected == predicted

    tests = list()

    for t in test_cases:
        expected = t
        predicted = subword_tokenizer.encode("".join(t), out_type=str)
        tests.append(
            {
                "expected": expected,
                "predicted": predicted,
                "pass": _check_test(expected, predicted),
            }
        )

    return tests


class TestReport:
    """Class purpose is to create an object that allows you to add 
    vocabulary tests as rows of a Pandas' Dataframe.

    This class is deprecated. Compatibility has been broken with new
    problem classes. It might be useful to give ideas for the curriculum
    report mechanism. Eventually will be removed.
    """

    results = pd.DataFrame()

    def add_test(self, test: list, label: str = None, test_type: str = None):
        """This method allows to add the tests to the object 
        created with TestReport(). Each time the add_test() 
        method is executed, a row is added to the Dataframe.

        Args:
            test(list): is the output of the classes.
            label(str): Optional strings shown in each row of 
                the table. None value by default. 
            test_type(str): Optional strings shown in each row 
                of the table. None value by default.       
        """
        df = pd.DataFrame(test)
        label = label
        success = df["pass"].sum()
        fail = (~df["pass"]).sum()
        total = len(df)
        success_ratio = success / total * 100
        examples = list(df[~df["pass"]].predicted[:7])
        columns = [
            "test_type",
            "label",
            "successful",
            "failed",
            "total tests",
            "% pass",
            "examples of failed",
        ]
        data = [
            [test_type, label, success, fail, total, success_ratio, examples]
        ]
        test_df = pd.DataFrame(data, columns=columns)
        self.results = self.results.append(test_df).reset_index(drop=True)

    def print_results(self):
        """Prints the results from the 'add_test method'.
        """
        print(self.results, sep="\n")
