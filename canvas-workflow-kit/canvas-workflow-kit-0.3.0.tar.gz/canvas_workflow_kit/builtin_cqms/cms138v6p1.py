from typing import List

from canvas_workflow_kit.builtin_cqms.cms138v6_preventive_care_and_screening_tobacco_use_screening_and_cessation_intervention import (
    ClinicalQualityMeasure138v6,
    TobaccoUseScreening,
    InterviewRecommendation,
    ProtocolResult,
    events,
    STATUS_DUE,
    STATUS_NOT_APPLICABLE,
)


class ClinicalQualityMeasure138v6p1(ClinicalQualityMeasure138v6):
    """
    Use only the Population 1's path of the ClinicalQualityMeasure138v6
    """

    title = 'Preventive Care and Screening: Tobacco Use: Screening'

    description = 'Patients aged 18 years and older who have not been screened for tobacco use in the last year.'
    information = 'https://ecqi.healthit.gov/ecqm/measures/cms138v6'

    identifiers = ['CMS138v6p1']

    types = ['CQM']

    responds_to_event_types = [
        events.HEALTH_MAINTENANCE,
    ]

    authors = []

    @property
    def references(self) -> List[str]:
        return [
            'Siu AL; U.S. Preventive Services Task Force. Behavioral and Pharmacotherapy Interventions for Tobacco Smoking Cessation in Adults, Including Pregnant Women: U.S. Preventive Services Task Force Recommendation Statement. Ann Intern Med. 2015 Oct 20;163(8):622-34.',
        ]

    funding_source = ''

    compute_on_change_types = [
        ClinicalQualityMeasure138v6.CHANGE_PROTOCOL_OVERRIDE,
        ClinicalQualityMeasure138v6.CHANGE_BILLING_LINE_ITEM,
        ClinicalQualityMeasure138v6.CHANGE_INTERVIEW,
        ClinicalQualityMeasure138v6.CHANGE_PATIENT,
    ]

    @classmethod
    def revision(cls) -> str:
        return '2019-04-18v1'

    def in_initial_population(self) -> bool:
        super().in_initial_population()
        return self._populations[self.POPULATION_1].in_initial_population

    def in_denominator(self) -> bool:
        super().in_denominator()
        return self._populations[self.POPULATION_1].in_denominator

    def in_numerator(self) -> bool:
        super().in_numerator()
        return self._populations[self.POPULATION_1].in_numerator

    def compute_results(self) -> ProtocolResult:
        result = ProtocolResult()
        if self.in_denominator():
            self.in_numerator()
            if (self._populations[self.POPULATION_1].in_denominator and
                    not self._populations[self.POPULATION_1].in_numerator):
                result.due_in = -1
                result.status = STATUS_DUE
                result.add_narrative(
                    f'{self.patient.first_name} should be screened for tobacco use.')
                result.add_recommendation(
                    InterviewRecommendation(
                        key='CMS138v6p1_RECOMMEND_TOBACCO_USE_SCREENING',
                        rank=1,
                        button='Plan',
                        patient=self.patient,
                        questionnaires=[TobaccoUseScreening],
                        title='Complete tobacco use questionnaire'))

            elif self.tobacco_use_screening_non_user:
                self.satisfied_result(
                    self.tobacco_use_screening_non_user,
                    '{name} had a Tobacco screening {date} and is not a smoker.', result)

            elif self.tobacco_use_screening_user:
                self.satisfied_result(self.tobacco_use_screening_user,
                                      '{name} had a Tobacco screening {date} and is a smoker.',
                                      result)
        elif self.patient.age_at(self.timeframe.end) < self.MINIMUM_AGE:
            result.status = STATUS_NOT_APPLICABLE
            result.due_in = (
                self.patient.birthday.shift(years=self.MINIMUM_AGE) - self.timeframe.end).days
        return result
