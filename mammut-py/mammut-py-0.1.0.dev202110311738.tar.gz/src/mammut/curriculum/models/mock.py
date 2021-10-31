from mammut.curriculum.models import model_base
import mammut.curriculum.report as report
import time
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class TestMockModel(model_base.ModelBase):
    def __init__(self, course_id: int, lesson_id: int):
        model_base.ModelBase.__init__(self, {}, course_id, lesson_id)
        self.sleep_time = 20

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        time.sleep(self.sleep_time)

    def save(self, mammut_session_context: MammutSessionContext, **kwargs):
        model_file_system_path = self._get_model_file_system_path(
            mammut_session_context.curriculum_save_folder
        )
        report.send_message(
            report.CurriculumGeneralDebugMessage(
                f"Save TestMockModel model in: {model_file_system_path}"
            )
        )
        pass
