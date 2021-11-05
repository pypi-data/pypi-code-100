from whizbang.data.az_cli_context import AzCliContext
from whizbang.domain.models.active_directory.az_account import AzAccount
from whizbang.domain.repository.az.az_repository_base import AzRepositoryBase


class AzAccountRepository(AzRepositoryBase):
    def __init__(self, context: AzCliContext):
        AzRepositoryBase.__init__(self, context)

    @property
    def _resource_provider(self) -> str:
        return "account"

    def get_account(self) -> AzAccount:
        account_details: dict = self._execute("show")
        account = None
        if account_details is not None:
            account_type = account_details['user']['type']
            name = account_details['user']['name']
            account = AzAccount(account_type=account_type, name=name)
        return account

    def set_account(self, subscription: str):
        self._execute(f'set --subscription {subscription}')
