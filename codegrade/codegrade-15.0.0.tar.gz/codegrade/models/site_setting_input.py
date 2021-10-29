"""The module that defines the ``SiteSettingInput`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .assignment_default_grading_scale_setting import (
    AssignmentDefaultGradingScaleSetting,
)
from .at_image_caching_enabled_setting import AtImageCachingEnabledSetting
from .auto_test_capture_points_message_setting import (
    AutoTestCapturePointsMessageSetting,
)
from .auto_test_checkpoint_message_setting import (
    AutoTestCheckpointMessageSetting,
)
from .auto_test_code_quality_message_setting import (
    AutoTestCodeQualityMessageSetting,
)
from .auto_test_enabled_setting import AutoTestEnabledSetting
from .auto_test_heartbeat_interval_setting import (
    AutoTestHeartbeatIntervalSetting,
)
from .auto_test_heartbeat_max_missed_setting import (
    AutoTestHeartbeatMaxMissedSetting,
)
from .auto_test_io_test_message_setting import AutoTestIoTestMessageSetting
from .auto_test_io_test_sub_message_setting import (
    AutoTestIoTestSubMessageSetting,
)
from .auto_test_max_concurrent_batch_runs_setting import (
    AutoTestMaxConcurrentBatchRunsSetting,
)
from .auto_test_max_global_setup_time_setting import (
    AutoTestMaxGlobalSetupTimeSetting,
)
from .auto_test_max_jobs_per_runner_setting import (
    AutoTestMaxJobsPerRunnerSetting,
)
from .auto_test_max_per_student_setup_time_setting import (
    AutoTestMaxPerStudentSetupTimeSetting,
)
from .auto_test_max_result_not_started_setting import (
    AutoTestMaxResultNotStartedSetting,
)
from .auto_test_max_time_command_setting import AutoTestMaxTimeCommandSetting
from .auto_test_max_unit_test_metadata_length_setting import (
    AutoTestMaxUnitTestMetadataLengthSetting,
)
from .auto_test_run_program_message_setting import (
    AutoTestRunProgramMessageSetting,
)
from .auto_test_unit_test_message_setting import AutoTestUnitTestMessageSetting
from .automatic_lti_role_enabled_setting import AutomaticLtiRoleEnabledSetting
from .blackboard_zip_upload_enabled_setting import (
    BlackboardZipUploadEnabledSetting,
)
from .course_register_enabled_setting import CourseRegisterEnabledSetting
from .email_students_enabled_setting import EmailStudentsEnabledSetting
from .exam_login_max_length_setting import ExamLoginMaxLengthSetting
from .groups_enabled_setting import GroupsEnabledSetting
from .incremental_rubric_submission_enabled_setting import (
    IncrementalRubricSubmissionEnabledSetting,
)
from .jwt_access_token_expires_setting import JwtAccessTokenExpiresSetting
from .linters_enabled_setting import LintersEnabledSetting
from .login_token_before_time_setting import LoginTokenBeforeTimeSetting
from .lti_enabled_setting import LtiEnabledSetting
from .max_file_size_setting import MaxFileSizeSetting
from .max_large_upload_size_setting import MaxLargeUploadSizeSetting
from .max_lines_setting import MaxLinesSetting
from .max_mirror_file_age_setting import MaxMirrorFileAgeSetting
from .max_normal_upload_size_setting import MaxNormalUploadSizeSetting
from .max_number_of_files_setting import MaxNumberOfFilesSetting
from .max_plagiarism_matches_setting import MaxPlagiarismMatchesSetting
from .min_password_score_setting import MinPasswordScoreSetting
from .notification_poll_time_setting import NotificationPollTimeSetting
from .peer_feedback_enabled_setting import PeerFeedbackEnabledSetting
from .register_enabled_setting import RegisterEnabledSetting
from .release_message_max_time_setting import ReleaseMessageMaxTimeSetting
from .render_html_enabled_setting import RenderHtmlEnabledSetting
from .reset_token_time_setting import ResetTokenTimeSetting
from .rubrics_enabled_setting import RubricsEnabledSetting
from .server_time_diff_tolerance_setting import ServerTimeDiffToleranceSetting
from .setting_token_time_setting import SettingTokenTimeSetting
from .site_email_setting import SiteEmailSetting
from .student_payment_enabled_setting import StudentPaymentEnabledSetting

SiteSettingInput = t.Union[
    AutoTestMaxTimeCommandSetting,
    AutoTestHeartbeatIntervalSetting,
    AutoTestHeartbeatMaxMissedSetting,
    AutoTestMaxJobsPerRunnerSetting,
    AutoTestMaxConcurrentBatchRunsSetting,
    AutoTestIoTestMessageSetting,
    AutoTestIoTestSubMessageSetting,
    AutoTestRunProgramMessageSetting,
    AutoTestCapturePointsMessageSetting,
    AutoTestCheckpointMessageSetting,
    AutoTestUnitTestMessageSetting,
    AutoTestCodeQualityMessageSetting,
    AutoTestMaxResultNotStartedSetting,
    AutoTestMaxUnitTestMetadataLengthSetting,
    ExamLoginMaxLengthSetting,
    LoginTokenBeforeTimeSetting,
    MinPasswordScoreSetting,
    ResetTokenTimeSetting,
    SettingTokenTimeSetting,
    SiteEmailSetting,
    MaxNumberOfFilesSetting,
    MaxLargeUploadSizeSetting,
    MaxNormalUploadSizeSetting,
    MaxFileSizeSetting,
    JwtAccessTokenExpiresSetting,
    MaxLinesSetting,
    NotificationPollTimeSetting,
    ReleaseMessageMaxTimeSetting,
    MaxPlagiarismMatchesSetting,
    MaxMirrorFileAgeSetting,
    AutoTestMaxGlobalSetupTimeSetting,
    AutoTestMaxPerStudentSetupTimeSetting,
    ServerTimeDiffToleranceSetting,
    AssignmentDefaultGradingScaleSetting,
    BlackboardZipUploadEnabledSetting,
    RubricsEnabledSetting,
    AutomaticLtiRoleEnabledSetting,
    LtiEnabledSetting,
    LintersEnabledSetting,
    IncrementalRubricSubmissionEnabledSetting,
    RegisterEnabledSetting,
    GroupsEnabledSetting,
    AutoTestEnabledSetting,
    CourseRegisterEnabledSetting,
    RenderHtmlEnabledSetting,
    EmailStudentsEnabledSetting,
    PeerFeedbackEnabledSetting,
    AtImageCachingEnabledSetting,
    StudentPaymentEnabledSetting,
]
SiteSettingInputParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(AutoTestMaxTimeCommandSetting),
        ParserFor.make(AutoTestHeartbeatIntervalSetting),
        ParserFor.make(AutoTestHeartbeatMaxMissedSetting),
        ParserFor.make(AutoTestMaxJobsPerRunnerSetting),
        ParserFor.make(AutoTestMaxConcurrentBatchRunsSetting),
        ParserFor.make(AutoTestIoTestMessageSetting),
        ParserFor.make(AutoTestIoTestSubMessageSetting),
        ParserFor.make(AutoTestRunProgramMessageSetting),
        ParserFor.make(AutoTestCapturePointsMessageSetting),
        ParserFor.make(AutoTestCheckpointMessageSetting),
        ParserFor.make(AutoTestUnitTestMessageSetting),
        ParserFor.make(AutoTestCodeQualityMessageSetting),
        ParserFor.make(AutoTestMaxResultNotStartedSetting),
        ParserFor.make(AutoTestMaxUnitTestMetadataLengthSetting),
        ParserFor.make(ExamLoginMaxLengthSetting),
        ParserFor.make(LoginTokenBeforeTimeSetting),
        ParserFor.make(MinPasswordScoreSetting),
        ParserFor.make(ResetTokenTimeSetting),
        ParserFor.make(SettingTokenTimeSetting),
        ParserFor.make(SiteEmailSetting),
        ParserFor.make(MaxNumberOfFilesSetting),
        ParserFor.make(MaxLargeUploadSizeSetting),
        ParserFor.make(MaxNormalUploadSizeSetting),
        ParserFor.make(MaxFileSizeSetting),
        ParserFor.make(JwtAccessTokenExpiresSetting),
        ParserFor.make(MaxLinesSetting),
        ParserFor.make(NotificationPollTimeSetting),
        ParserFor.make(ReleaseMessageMaxTimeSetting),
        ParserFor.make(MaxPlagiarismMatchesSetting),
        ParserFor.make(MaxMirrorFileAgeSetting),
        ParserFor.make(AutoTestMaxGlobalSetupTimeSetting),
        ParserFor.make(AutoTestMaxPerStudentSetupTimeSetting),
        ParserFor.make(ServerTimeDiffToleranceSetting),
        ParserFor.make(AssignmentDefaultGradingScaleSetting),
        ParserFor.make(BlackboardZipUploadEnabledSetting),
        ParserFor.make(RubricsEnabledSetting),
        ParserFor.make(AutomaticLtiRoleEnabledSetting),
        ParserFor.make(LtiEnabledSetting),
        ParserFor.make(LintersEnabledSetting),
        ParserFor.make(IncrementalRubricSubmissionEnabledSetting),
        ParserFor.make(RegisterEnabledSetting),
        ParserFor.make(GroupsEnabledSetting),
        ParserFor.make(AutoTestEnabledSetting),
        ParserFor.make(CourseRegisterEnabledSetting),
        ParserFor.make(RenderHtmlEnabledSetting),
        ParserFor.make(EmailStudentsEnabledSetting),
        ParserFor.make(PeerFeedbackEnabledSetting),
        ParserFor.make(AtImageCachingEnabledSetting),
        ParserFor.make(StudentPaymentEnabledSetting),
    ),
)
