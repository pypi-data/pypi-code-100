import enum


class Phase:
    """Constants for typed phase description in messages.
    """

    LOAD_PACKAGE_DATA = "Load Package Data"
    LOAD_ASSESSMENT_DATA = "Load Assessment Data"
    LOAD_CURRICULUM_LESSONS_DATA = "Load Lessons Data"
    CREATE_CURRICULUM_FLOWCHART = "Create Curriculum Flowchart"
    CREATE_CLASSROOMS = "Create Classrooms"
    LECTURE_LESSON = "Lecture Lesson"


class Component(enum.Enum):
    """Component responsible for the message report.
    """

    Curriculum = 1
    Classroom = 2
    Course = 3
    Lesson = 4
    Problem = 5
    Package = 6
    LinguisticStandard = 7
