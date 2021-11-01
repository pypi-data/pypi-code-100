from typing import Optional

from lgt_data.engine import UserCreditStatementDocument, UserFeedLead
from lgt_data.mongo_repository import UserMongoRepository, to_object_id
from pydantic import BaseModel

from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
User balance handling
"""

class UpdateUserBalanceJobData(BaseBackgroundJobData, BaseModel):
    user_id: Optional[str]

class UpdateUserBalanceJob(BaseBackgroundJob):
    @property
    def job_data_type(self) -> type:
        return UpdateUserBalanceJobData

    @staticmethod
    def __update_processed(user_id: str):
        pipeline = [
            {
                "$match": {
                    "user_id": to_object_id(user_id),
                    "balance": {"$lte": 0}
                }
            },
            {
                '$group': {
                    '_id': "$user_id",
                    'count': {'$sum': {"$multiply": [-1, "$balance"]}}
                }
            }
        ]

        results = list(UserCreditStatementDocument.objects.aggregate(*pipeline))
        if not results:
            return

        count = results[0]["count"]
        UserMongoRepository().set(user_id, leads_proceeded=count)

    @staticmethod
    def __update_filtered(user_id: str):
        count = UserFeedLead.objects(user_id=to_object_id(user_id)).count()
        UserMongoRepository().set(user_id, leads_filtered=count)

    def exec(self, data: UpdateUserBalanceJobData):
        user = UserMongoRepository().get(data.user_id)
        if not user:
            return

        self.__update_processed(user_id=data.user_id)
        self.__update_filtered(user_id=data.user_id)


