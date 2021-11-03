from whizbang.domain.manager.az.az_manager_base import AzManagerBase
from whizbang.domain.models.active_directory.az_account import AzAccount
from whizbang.domain.repository.az.az_account_repository import AzAccountRepository


class AzAccountManager(AzManagerBase):
    def __init__(self, repository: AzAccountRepository):
        super().__init__(repository)
        self._repository: AzAccountRepository = self._repository

    def get_account(self) -> AzAccount:
        return self._repository.get_account()

    def set_account(self, subscription: str):
        return self._repository.set_account(subscription=subscription)
