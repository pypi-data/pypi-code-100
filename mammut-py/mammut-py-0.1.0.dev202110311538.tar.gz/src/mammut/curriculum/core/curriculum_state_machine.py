import transitions


class CurriculumStateMachineMixin(object):
    """Models the finite state machine for a concrete Curriculum
    learning experience.

    Note: This is a separate class, but some transitions are tightly coupled
    to the curriculum concrete class. This is so, because some transitions
    will call curriculum methods "on_enter"/"on_exit".
    """

    # States
    """
        Unprepared state after instantiation. 
        Call load method for transition.
    """
    STATE_UNPREPARED = "unprepared"

    """
        Ready after loaded.
    """
    STATE_READY = transitions.State(
        name="ready", on_enter="_compute_next_academic_period"
    )

    """
        When assigned, the curriculum automatically 
        will process the courses for the assigned academic period.
    """
    STATE_ASSIGNED = transitions.State(
        name="assigned", on_enter="_take_courses"
    )

    """
        Completed when all courses has been approved.
    """
    STATE_COMPLETED = "completed"

    """
        Currently, a curriculum is failed if:
            - A course can't be approved.
    """
    STATE_FAILED = "failed"

    STATES = [
        STATE_UNPREPARED,
        STATE_READY,
        STATE_ASSIGNED,
        STATE_COMPLETED,
        STATE_FAILED,
    ]

    # Transitions
    PREPARE_TRIGGER = "prepare"
    BEGIN_COURSES_TRIGGER = "begin_courses"
    ASSIGNED_COURSES_COMPLETED_TRIGGER = "assigned_courses_completed"
    CURRICULUM_COMPLETED_TRIGGER = "assigned_courses_evaluated"
    FAIL_COURSE_TRIGGER = "fail_course"

    PREPARE_TRANSITION = {
        "trigger": PREPARE_TRIGGER,
        "source": STATE_UNPREPARED,
        "dest": STATE_READY,
    }
    BEGIN_COURSES_TRANSITION = {
        "trigger": BEGIN_COURSES_TRIGGER,
        "source": STATE_READY,
        "dest": STATE_ASSIGNED,
    }
    COMPLETED_TRANSITION = {
        "trigger": CURRICULUM_COMPLETED_TRIGGER,
        "source": STATE_READY,
        "dest": STATE_COMPLETED,
    }
    COURSES_COMPLETED_TRANSITION = {
        "trigger": ASSIGNED_COURSES_COMPLETED_TRIGGER,
        "source": STATE_ASSIGNED,
        "dest": STATE_READY,
    }
    COURSE_FAILED_TRANSITION = {
        "trigger": FAIL_COURSE_TRIGGER,
        "source": STATE_READY,
        "dest": STATE_FAILED,
    }

    TRANSITIONS = [
        PREPARE_TRANSITION,
        BEGIN_COURSES_TRANSITION,
        COMPLETED_TRANSITION,
        COURSES_COMPLETED_TRANSITION,
        COURSE_FAILED_TRANSITION,
    ]

    def __init__(self):
        self.machine = transitions.Machine(
            model=self,
            states=self.STATES,
            transitions=self.TRANSITIONS,
            initial=self.STATE_UNPREPARED,
        )
        super(CurriculumStateMachineMixin, self).__init__()
