from typing import List, Dict
from mammut.curriculum.course.course import (
    Course,
    KttPackageInterpretationCourse,
)
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
import mammut.curriculum.core.utils as curriculum_utils
import mammut.curriculum.report as report
import networkx as nx


class Flowchart:
    """Encapsulates graph structure for the curriculum shape.

        Class invariants:
            - The curriculum flowchart is a directed acyclic graph.
            - Isolated courses are not allowed.
            - Courses ID's are only allowed to be integers.
    """

    def __init__(self, curriculum: "CurriculumBase"):
        """
        Args:
            curriculum: Curriculum object to get references from.
        """
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(curriculum.courses)
        self.valid = True
        self.errors: List[str] = []
        """
            Creates a local dictionary for id->node(course object).
            Used in second iteration to add the directed edge from a prerequisite 
            node to the prelate node. 
        """
        self.graph_dict: Dict = {}
        for course in curriculum.courses:
            self.graph_dict[course.course_id] = course
        for course in curriculum.courses:
            for prerequisite in course.prerequisites:
                self.graph.add_edge(self.graph_dict[prerequisite], course)

        """
            Perform validations to the flowchart shape. 
            If an error is found, flowchart is marked invalid, 
            and errors can be requested in curriculum client class.
        """
        if not nx.algorithms.isolate.number_of_isolates(self.graph) == 0:
            self.valid = False
            error_message_str = f"""Curriculum contains isolated courses {
                [course.course_id for course in nx.algorithms.isolate.isolates(self.graph)]
                }"""
            report.send_message(
                report.CurriculumGeneralErrorMessage(error_message_str)
            )
            self.errors.append(error_message_str)

        if not nx.algorithms.dag.is_directed_acyclic_graph(self.graph):
            self.valid = False
            error_message_str = "Curriculum flowchart contains cycles."
            report.send_message(
                report.CurriculumGeneralErrorMessage(error_message_str)
            )
            self.errors.append(error_message_str)

    def add_ktt_interpretation_course(self, curriculum: "CurriculumBase"):
        """Adds the KtT compilation interpretation course as the first course
        of the curriculum, in the academic period 0.

        It also adds the course as prerequisite to all the courses from the academic
        period 1.
        """
        ktt_package_course = KttPackageInterpretationCourse(
            curriculum._mammut_session_context, curriculum.assessor
        )
        curriculum.courses.insert(0, ktt_package_course)
        first_academic_period_courses = [
            course
            for course in curriculum.courses
            if course.academic_period == 1
        ]
        for course in first_academic_period_courses:
            course.prerequisites = [0]

        self.graph_dict[ktt_package_course.course_id] = ktt_package_course
        for course in first_academic_period_courses:
            self.graph.add_edge(
                self.graph_dict[ktt_package_course.course_id], course
            )

    def get_max_parallel_courses(self) -> int:
        """Returns the maximum number of parallel courses in the academic
        periods.
        """
        academic_periods_table: Dict = {}
        for c in self.graph.nodes:
            if c.academic_period not in academic_periods_table:
                academic_periods_table[c.academic_period] = 1
            else:
                academic_periods_table[c.academic_period] += 1

        return max(academic_periods_table.values())
