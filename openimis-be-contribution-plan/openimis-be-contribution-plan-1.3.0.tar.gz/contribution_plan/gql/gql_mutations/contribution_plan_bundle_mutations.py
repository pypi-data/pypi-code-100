from core.gql.gql_mutations import DeleteInputType
from core.gql.gql_mutations.base_mutation import BaseMutation, BaseDeleteMutation, BaseReplaceMutation, \
    BaseHistoryModelCreateMutationMixin, BaseHistoryModelUpdateMutationMixin, \
    BaseHistoryModelDeleteMutationMixin, BaseHistoryModelReplaceMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanBundleInputType, ContributionPlanBundleUpdateInputType, \
    ContributionPlanBundleReplaceInputType
from contribution_plan.models import ContributionPlanBundle


class CreateContributionPlanBundleMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleInputType):
        pass


class UpdateContributionPlanBundleMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleUpdateInputType):
        pass


class DeleteContributionPlanBundleMutation(BaseHistoryModelDeleteMutationMixin, BaseDeleteMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanBundleMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleReplaceInputType):
        pass