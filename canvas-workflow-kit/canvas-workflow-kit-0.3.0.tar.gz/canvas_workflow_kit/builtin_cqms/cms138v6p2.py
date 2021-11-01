from typing import List

from canvas_workflow_kit.builtin_cqms.cms138v6_preventive_care_and_screening_tobacco_use_screening_and_cessation_intervention import (
    ClinicalQualityMeasure138v6,
    TobaccoUseCessationCounseling,
    TobaccoUseCessationPharmacotherapy,
    InstructionRecommendation,
    PrescribeRecommendation,
    ProtocolResult,
    events,
    STATUS_DUE,
    STATUS_NOT_APPLICABLE,
)


class ClinicalQualityMeasure138v6p2(ClinicalQualityMeasure138v6):
    """
    Use only the Population 2's path of the ClinicalQualityMeasure138v6
    """

    title = 'Preventive Care and Screening: Tobacco Use: Cessation Intervention'

    description = ('Patients aged 18 years and older, and identified as a tobacco user, '
                   'who have not received tobacco cessation intervention such as counselling, '
                   'referral or medication.')
    information = 'https://ecqi.healthit.gov/ecqm/measures/cms138v6'

    identifiers = ['CMS138v6p2']

    types = ['CQM']

    responds_to_event_types = [
        events.HEALTH_MAINTENANCE,
    ]

    authors = [
        'American Medical Association (AMA)',
        'PCPI(R) Foundation (PCPI[R])',
    ]

    @property
    def references(self) -> List[str]:
        return [
            'Siu AL; U.S. Preventive Services Task Force. Behavioral and Pharmacotherapy Interventions for Tobacco Smoking Cessation in Adults, Including Pregnant Women: U.S. Preventive Services Task Force Recommendation Statement. Ann Intern Med. 2015 Oct 20;163(8):622-34.',
        ]

    funding_source = ''

    compute_on_change_types = [
        ClinicalQualityMeasure138v6.CHANGE_PROTOCOL_OVERRIDE,
        ClinicalQualityMeasure138v6.CHANGE_BILLING_LINE_ITEM,
        ClinicalQualityMeasure138v6.CHANGE_INSTRUCTION,
        ClinicalQualityMeasure138v6.CHANGE_INTERVIEW,
        ClinicalQualityMeasure138v6.CHANGE_MEDICATION,
        ClinicalQualityMeasure138v6.CHANGE_PATIENT,
    ]

    @classmethod
    def revision(cls) -> str:
        return '2019-04-18v1'

    def in_initial_population(self) -> bool:
        super().in_initial_population()
        return self._populations[self.POPULATION_2].in_initial_population

    def in_denominator(self) -> bool:
        super().in_denominator()
        return self._populations[self.POPULATION_2].in_denominator

    def in_numerator(self) -> bool:
        super().in_numerator()
        return self._populations[self.POPULATION_2].in_numerator

    def compute_results(self) -> ProtocolResult:
        result = ProtocolResult()
        if self.in_denominator():
            self.in_numerator()
            if (self._populations[self.POPULATION_2].in_denominator and
                    not self._populations[self.POPULATION_2].in_numerator):
                result.due_in = -1
                result.status = STATUS_DUE
                result.add_narrative(f'{self.patient.first_name} is a current tobacco user, '
                                     f'intervention is indicated.')
                result.add_recommendation(
                    InstructionRecommendation(
                        key='CMS138v6p2_RECOMMEND_CESSATION_COUNSELING',
                        rank=1,
                        button='Plan',
                        patient=self.patient,
                        instruction=TobaccoUseCessationCounseling,
                        title='Tobacco cessation counseling'))
                result.add_recommendation(
                    PrescribeRecommendation(
                        key='CMS138v6p2_RECOMMEND_CESSATION_MEDICATION',
                        rank=2,
                        button='Plan',
                        patient=self.patient,
                        prescription=TobaccoUseCessationPharmacotherapy,
                        title='Cessation support medication'))
            elif self.tobacco_cessation_intervention_counseling:
                self.satisfied_result(self.tobacco_cessation_intervention_counseling,
                                      '{name} had a smoking cessation counseling {date}.', result)
            elif self.tobacco_cessation_intervention_medication:
                self.satisfied_result(self.tobacco_cessation_intervention_medication,
                                      '{name} has been prescribed cessation medication {date}.',
                                      result)
        elif self.patient.age_at(self.timeframe.end) < self.MINIMUM_AGE:
            result.status = STATUS_NOT_APPLICABLE
            result.due_in = (
                self.patient.birthday.shift(years=self.MINIMUM_AGE) - self.timeframe.end).days
        return result
